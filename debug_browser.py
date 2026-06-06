from patchright.sync_api import sync_playwright

p = sync_playwright().start()
browser = p.chromium.launch(
    headless=False,
    args=[
        "--remote-debugging-port=9222",
        "--start-maximized",
    ],
)
context = browser.new_context(no_viewport=True)
page = context.new_page()
page.goto("https://account.proton.me/signup?plan=free&billing=24&currency=EUR&language=en")

print("浏览器已启动，CDP 端口: 9222")
print("按回车关闭浏览器...")
input()

browser.close()
p.stop()
