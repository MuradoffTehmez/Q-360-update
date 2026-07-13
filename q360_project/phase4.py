import re
import os

# 1. Update navbar.html
navbar_path = 'templates/base/navbar.html'
with open(navbar_path, 'r', encoding='utf-8') as f:
    nav = f.read()

# Background
nav = nav.replace('bg-gradient-to-r from-blue-600 to-indigo-700 dark:from-gray-800 dark:to-gray-900', 'bg-white dark:bg-gray-900')
# Text colors
nav = nav.replace('text-white hover:text-blue-100', 'text-gray-900 dark:text-white hover:text-blue-600 dark:hover:text-blue-400')
nav = nav.replace('text-white hover:bg-white/10', 'text-gray-900 dark:text-white hover:bg-gray-100 dark:hover:bg-gray-800')
nav = nav.replace('text-blue-200', 'text-gray-500 dark:text-gray-400')
nav = nav.replace('bg-white p-1.5', 'bg-blue-50 dark:bg-gray-800 p-1.5')

# Feedback button should stay colored
nav = nav.replace('text-gray-900 dark:text-white rounded-lg shadow-md', 'text-white rounded-lg shadow-md')

# Mobile menu toggle
nav = nav.replace('p-1.5 text-gray-900 dark:text-white hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition-all duration-200 ml-1', 
                  'p-1.5 text-gray-900 dark:text-white hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition-all duration-200 ml-1')

# Write navbar
with open(navbar_path, 'w', encoding='utf-8') as f:
    f.write(nav)

# 2. Update dashboard.html (Stat Cards & Active Tasks)
dash_path = 'templates/accounts/dashboard.html'
with open(dash_path, 'r', encoding='utf-8') as f:
    dash = f.read()

# Stat cards titles
dash = dash.replace('text-gray-600 dark:text-gray-400 uppercase', 'text-gray-800 dark:text-gray-200 uppercase font-bold')

# Stat number CSS to ensure visibility in light mode
dash = re.sub(r'\.stat-number \{', '.stat-number {\n        color: #1f2937;\n        .dark & { color: #f9fafb; }', dash)
# Ensure inline dark text
dash = dash.replace('text-3xl font-bold text-red-500', 'text-3xl font-bold text-red-300 dark:text-red-400')
dash = dash.replace('text-3xl font-bold text-blue-500', 'text-3xl font-bold text-blue-300 dark:text-blue-400')
dash = dash.replace('text-3xl font-bold text-purple-500', 'text-3xl font-bold text-purple-300 dark:text-purple-400')

# Quick actions background
dash = dash.replace('bg-white dark:bg-gray-800 rounded-xl shadow-soft', 'bg-gray-50 dark:bg-gray-800 rounded-xl shadow-sm')

# Fix N/A condition for Avg Score
avg_block = """{% if average_score and average_score != 'N/A' and average_score != 0 %}"""
new_avg_block = """{% if average_score and average_score != 'N/A' and average_score != '0' and average_score != 0 %}"""
dash = dash.replace(avg_block, new_avg_block)

# Add chart theme sync script at the end
chart_script = """
<script>
// Watch for theme changes
const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
        if (mutation.attributeName === 'class') {
            const isDark = document.documentElement.classList.contains('dark');
            const textColor = isDark ? '#e2e8f0' : '#475569';
            const gridColor = isDark ? '#334155' : '#e2e8f0';
            
            // Update all charts if Chart is defined
            if (typeof Chart !== 'undefined') {
                Chart.instances.forEach(chart => {
                    if (chart.options.scales) {
                        if (chart.options.scales.x) {
                            chart.options.scales.x.ticks.color = textColor;
                            chart.options.scales.x.grid.color = gridColor;
                        }
                        if (chart.options.scales.y) {
                            chart.options.scales.y.ticks.color = textColor;
                            chart.options.scales.y.grid.color = gridColor;
                        }
                    }
                    if (chart.options.plugins && chart.options.plugins.legend) {
                        chart.options.plugins.legend.labels.color = textColor;
                    }
                    chart.update();
                });
            }
        }
    });
});
observer.observe(document.documentElement, { attributes: true });
</script>
"""
if "MutationObserver" not in dash:
    dash = dash + chart_script

with open(dash_path, 'w', encoding='utf-8') as f:
    f.write(dash)

# 3. Sidebar Accordion
side_path = 'templates/base/sidebar.html'
with open(side_path, 'r', encoding='utf-8') as f:
    side = f.read()

# Remove x-data="{ open: false }" from individual groups
side = side.replace('x-data="{ open: false }"', '')
side = side.replace('x-data="{ open: true }"', '')

# Wrap in activeAccordion x-data
side = side.replace('<div class="flex flex-col h-full">', '<div class="flex flex-col h-full" x-data="{ activeAccordion: null }">')

# Replace x-data="{ open: false }" with activeAccordion logic for each group
# We will just replace @click="open = !open" and x-show="open" dynamically using regex, but since we don't have x-data="{open: false}" explicitly on every item (they seem to inherit it or it's implicitly there?), let's find @click="open = !open"
def replace_accordion(m):
    idx = m.start()
    return f"@click=\"activeAccordion = activeAccordion === 'acc_{idx}' ? null : 'acc_{idx}'\""

side = re.sub(r'@click="open = !open"', replace_accordion, side)

def replace_show(m):
    # Find the corresponding acc_idx? It's hard with regex.
    # Let's just do a manual replace by counting.
    pass

# Simpler accordion logic: 
# Since there are multiple groups, let's just find them all and assign unique IDs
groups = side.split('@click="open = !open"')
if len(groups) > 1:
    new_side = groups[0]
    for i, g in enumerate(groups[1:]):
        new_side += f"@click=\"activeAccordion = activeAccordion === 'acc_{i}' ? null : 'acc_{i}'\"" + g
    
    # Now replace x-show="open"
    shows = new_side.split('x-show="open"')
    if len(shows) > 1:
        final_side = shows[0]
        for i, s in enumerate(shows[1:]):
            # The rotate class also uses open: :class="{'rotate-180': open}"
            # Let's replace 'open' in the string segment up to the next button
            segment = s.replace(":class=\"{'rotate-180': open}\"", f":class=\"{{'rotate-180': activeAccordion === 'acc_{i}'}}\"")
            final_side += f"x-show=\"activeAccordion === 'acc_{i}'\"" + segment
        side = final_side

with open(side_path, 'w', encoding='utf-8') as f:
    f.write(side)

# 4. Translations
# We will do a mass replace for missing translations
def tr(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        c = f.read()
    c = c.replace('{% trans "Feedback" %}', '{% trans "Rəy bildir" %}')
    c = c.replace('{% trans "Platform" %}', '{% trans "Platforma" %}')
    c = c.replace('{% trans "Resources" %}', '{% trans "Resurslar" %}')
    c = c.replace('{% trans "View All" %}', '{% trans "Hamısına Bax" %}')
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(c)

tr('templates/base/navbar.html')
tr('templates/base/footer.html')
tr('templates/accounts/dashboard.html')

print("Phase 4 fixes applied.")
