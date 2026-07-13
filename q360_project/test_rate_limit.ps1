for ($i = 1; $i -le 20; $i++) {
    try {
        $res = Invoke-WebRequest -Uri 'https://spoken-seltzer-reword.ngrok-free.dev/accounts/login/' -Method GET
        Write-Host "Request $i : $($res.StatusCode)"
    } catch {
        Write-Host "Request $i : $($_.Exception.Response.StatusCode.value__)"
    }
}
