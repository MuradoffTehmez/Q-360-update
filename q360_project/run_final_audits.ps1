$urls = @(
    @{ url = "http://localhost:8000/"; name = "landing" },
    @{ url = "http://localhost:8000/haqqimizda/"; name = "haqqimizda" },
    @{ url = "http://localhost:8000/faq/"; name = "faq" }
)

foreach ($item in $urls) {
    Write-Host "Running Desktop for $($item.name)..."
    npx lighthouse $($item.url) --output json --output-path "lighthouse-reports/final-$($item.name)-desktop.json" --preset desktop --only-categories=performance,accessibility,best-practices,seo
    
    # Retry logic specifically for desktop FAQ if it fails
    if ($item.name -eq "faq") {
        $maxRetries = 3
        $retryCount = 0
        while ($retryCount -lt $maxRetries) {
            $content = Get-Content "lighthouse-reports/final-faq-desktop.json" -Raw | ConvertFrom-Json
            if ($null -ne $content.runtimeError -and $content.runtimeError.code -eq "NO_NAVSTART") {
                Write-Host "NO_NAVSTART on FAQ desktop. Retrying ($retryCount)..."
                npx lighthouse $($item.url) --output json --output-path "lighthouse-reports/final-$($item.name)-desktop.json" --preset desktop --only-categories=performance,accessibility,best-practices,seo
                $retryCount++
            } else {
                break
            }
        }
    }

    Write-Host "Running Mobile for $($item.name)..."
    npx lighthouse $($item.url) --output json --output-path "lighthouse-reports/final-$($item.name)-mobile.json" --form-factor mobile --only-categories=performance,accessibility,best-practices,seo
}
Write-Host "All audits completed!"
