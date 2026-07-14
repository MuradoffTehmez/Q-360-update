import os
import re

file_path = r'c:\Users\Tahmaz Muradov\Desktop\Q-360\q360_project\templates\base\sidebar.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# For Dashboard (Batch 3)
dashboard_section = r'''
                    <a href="{% url 'dashboard:export_model' %}"
                        class="flex items-center px-3 py-2 text-sm font-semibold rounded-lg transition-all duration-200 relative overflow-hidden group {% if '/export-model' in request.path %}bg-gradient-to-r from-blue-50 to-blue-100 dark:from-blue-900/30 dark:to-blue-800/30 text-blue-700 dark:text-blue-400 border-l-4 border-blue-500{% else %}text-gray-900 font-bold dark:text-white hover:bg-gradient-to-r hover:from-gray-50 hover:to-gray-100 dark:hover:from-gray-700 dark:hover:to-gray-600/50{% endif %}">
                        <i class="fas fa-file-export w-6 text-center relative z-10 flex-shrink-0 text-lg transition-all" :class="sidebarOpen ? 'mr-3' : 'mx-auto text-xl'"></i><span class="relative z-10 flex-1 whitespace-normal leading-tight" x-show="sidebarOpen">Export</span>
                    </a>
'''
if 'export_model' not in content:
    content = content.replace('{% trans "Panel və Analitika" %}</span>\n                    </span>', '{% trans "Panel və Analitika" %}</span>\n                    </span>').replace(
        '<a href="{% url \'dashboard:executive\' %}"',
        dashboard_section + '\n                    <a href="{% url \'dashboard:executive\' %}"'
    )

# For Evaluations (Batch 4)
eval_section = r'''
                    <a href="{% url 'evaluations:question-list' %}"
                        class="flex items-center px-3 py-2 text-sm font-semibold rounded-lg transition-all duration-200 relative overflow-hidden group {% if '/questions' in request.path %}bg-gradient-to-r from-blue-50 to-blue-100 dark:from-blue-900/30 dark:to-blue-800/30 text-blue-700 dark:text-blue-400 border-l-4 border-blue-500{% else %}text-gray-900 font-bold dark:text-white hover:bg-gradient-to-r hover:from-gray-50 hover:to-gray-100 dark:hover:from-gray-700 dark:hover:to-gray-600/50{% endif %}">
                        <i class="fas fa-list-alt w-6 text-center relative z-10 flex-shrink-0 text-lg transition-all" :class="sidebarOpen ? 'mr-3' : 'mx-auto text-xl'"></i><span class="relative z-10 flex-1 whitespace-normal leading-tight" x-show="sidebarOpen">Forms & Questions</span>
                    </a>
                    <a href="{% url 'evaluations:review-cycles' %}"
                        class="flex items-center px-3 py-2 text-sm font-semibold rounded-lg transition-all duration-200 relative overflow-hidden group {% if '/review-cycles' in request.path %}bg-gradient-to-r from-blue-50 to-blue-100 dark:from-blue-900/30 dark:to-blue-800/30 text-blue-700 dark:text-blue-400 border-l-4 border-blue-500{% else %}text-gray-900 font-bold dark:text-white hover:bg-gradient-to-r hover:from-gray-50 hover:to-gray-100 dark:hover:from-gray-700 dark:hover:to-gray-600/50{% endif %}">
                        <i class="fas fa-sync w-6 text-center relative z-10 flex-shrink-0 text-lg transition-all" :class="sidebarOpen ? 'mr-3' : 'mx-auto text-xl'"></i><span class="relative z-10 flex-1 whitespace-normal leading-tight" x-show="sidebarOpen">Review Cycles</span>
                    </a>
                    <a href="{% url 'evaluations:templates' %}"
                        class="flex items-center px-3 py-2 text-sm font-semibold rounded-lg transition-all duration-200 relative overflow-hidden group {% if '/templates' in request.path %}bg-gradient-to-r from-blue-50 to-blue-100 dark:from-blue-900/30 dark:to-blue-800/30 text-blue-700 dark:text-blue-400 border-l-4 border-blue-500{% else %}text-gray-900 font-bold dark:text-white hover:bg-gradient-to-r hover:from-gray-50 hover:to-gray-100 dark:hover:from-gray-700 dark:hover:to-gray-600/50{% endif %}">
                        <i class="fas fa-file-contract w-6 text-center relative z-10 flex-shrink-0 text-lg transition-all" :class="sidebarOpen ? 'mr-3' : 'mx-auto text-xl'"></i><span class="relative z-10 flex-1 whitespace-normal leading-tight" x-show="sidebarOpen">Templates</span>
                    </a>
'''
if 'evaluations:question-list' not in content:
    content = content.replace('<a href="{% url \'evaluations:my-assignments\' %}"', eval_section + '\n                    <a href="{% url \'evaluations:my-assignments\' %}"')

# For Notifications (Batch 8)
notif_section = r'''
                    <a href="{% url 'notifications:sms-templates' %}"
                        class="flex items-center px-3 py-2 text-sm font-semibold rounded-lg transition-all duration-200 relative overflow-hidden group {% if '/sms-templates' in request.path %}bg-gradient-to-r from-blue-50 to-blue-100 dark:from-blue-900/30 dark:to-blue-800/30 text-blue-700 dark:text-blue-400 border-l-4 border-blue-500{% else %}text-gray-900 font-bold dark:text-white hover:bg-gradient-to-r hover:from-gray-50 hover:to-gray-100 dark:hover:from-gray-700 dark:hover:to-gray-600/50{% endif %}">
                        <i class="fas fa-sms w-6 text-center relative z-10 flex-shrink-0 text-lg transition-all" :class="sidebarOpen ? 'mr-3' : 'mx-auto text-xl'"></i><span class="relative z-10 flex-1 whitespace-normal leading-tight" x-show="sidebarOpen">SMS Templates</span>
                    </a>
                    <a href="{% url 'notifications:push-templates' %}"
                        class="flex items-center px-3 py-2 text-sm font-semibold rounded-lg transition-all duration-200 relative overflow-hidden group {% if '/push-templates' in request.path %}bg-gradient-to-r from-blue-50 to-blue-100 dark:from-blue-900/30 dark:to-blue-800/30 text-blue-700 dark:text-blue-400 border-l-4 border-blue-500{% else %}text-gray-900 font-bold dark:text-white hover:bg-gradient-to-r hover:from-gray-50 hover:to-gray-100 dark:hover:from-gray-700 dark:hover:to-gray-600/50{% endif %}">
                        <i class="fas fa-mobile-alt w-6 text-center relative z-10 flex-shrink-0 text-lg transition-all" :class="sidebarOpen ? 'mr-3' : 'mx-auto text-xl'"></i><span class="relative z-10 flex-1 whitespace-normal leading-tight" x-show="sidebarOpen">Push Templates</span>
                    </a>
                    <a href="{% url 'notifications:webhooks' %}"
                        class="flex items-center px-3 py-2 text-sm font-semibold rounded-lg transition-all duration-200 relative overflow-hidden group {% if '/webhooks' in request.path %}bg-gradient-to-r from-blue-50 to-blue-100 dark:from-blue-900/30 dark:to-blue-800/30 text-blue-700 dark:text-blue-400 border-l-4 border-blue-500{% else %}text-gray-900 font-bold dark:text-white hover:bg-gradient-to-r hover:from-gray-50 hover:to-gray-100 dark:hover:from-gray-700 dark:hover:to-gray-600/50{% endif %}">
                        <i class="fas fa-link w-6 text-center relative z-10 flex-shrink-0 text-lg transition-all" :class="sidebarOpen ? 'mr-3' : 'mx-auto text-xl'"></i><span class="relative z-10 flex-1 whitespace-normal leading-tight" x-show="sidebarOpen">Webhooks</span>
                    </a>
                    <a href="{% url 'notifications:queue' %}"
                        class="flex items-center px-3 py-2 text-sm font-semibold rounded-lg transition-all duration-200 relative overflow-hidden group {% if '/queue' in request.path %}bg-gradient-to-r from-blue-50 to-blue-100 dark:from-blue-900/30 dark:to-blue-800/30 text-blue-700 dark:text-blue-400 border-l-4 border-blue-500{% else %}text-gray-900 font-bold dark:text-white hover:bg-gradient-to-r hover:from-gray-50 hover:to-gray-100 dark:hover:from-gray-700 dark:hover:to-gray-600/50{% endif %}">
                        <i class="fas fa-layer-group w-6 text-center relative z-10 flex-shrink-0 text-lg transition-all" :class="sidebarOpen ? 'mr-3' : 'mx-auto text-xl'"></i><span class="relative z-10 flex-1 whitespace-normal leading-tight" x-show="sidebarOpen">Notification Queue</span>
                    </a>
'''
if 'notifications:sms-templates' not in content:
    content = content.replace('<a href="{% url \'notifications:test\' %}"', notif_section + '\n                    <a href="{% url \'notifications:test\' %}"')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated sidebar.html with missing links.")
