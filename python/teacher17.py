from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def save_page_source_selenium(url, output_file="output.html"):
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(url)

        # 使用显式等待，等待直到 id 为 dynamic-content 的元素可见
        wait = WebDriverWait(driver, 10)
        wait.until(EC.visibility_of_element_located((By.ID, "dynamic-content")))

        # 切换到iframe，如果有的话
        iframe_elements = driver.find_elements(By.TAG_NAME, "iframe")
        for iframe_element in iframe_elements:
            driver.switch_to.frame(iframe_element)

            # 在每个iframe中执行等待和操作
            wait.until(EC.visibility_of_element_located((By.ID, "dynamic-content")))
            time.sleep(5)

            # 获取iframe内部的页面源码
            page_source = driver.page_source

            # 切换回主文档
            driver.switch_to.default_content()

            with open(output_file, "w", encoding="utf-8") as file:
                file.write(page_source)

    except Exception as e:
        print(f"发生异常：{str(e)}")

    finally:
        driver.quit()


# 调用函数
links = [
    "https://szw.njfu.edu.cn/sclass_type.asp?id=566",
    # "https.s://szw.njfu.edu.cn/sclass_type.asp?id=567",
    # "https://szw.njfu.edu.cn/sclass_type.asp?id=568",
]

for i, url in enumerate(links, start=1):
    output_file_name = f"output_{i}.html"
    print(f"正在保存页面 {url} 的源码到文件: {output_file_name}")
    save_page_source_selenium(url, output_file_name)
    print("=" * 50)
