from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def crawl_webpage_and_extract_hrefs(url, output_file="output.txt"):
    # 启动Chrome浏览器
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # 无头模式
    driver = webdriver.Chrome(options=options)

    try:
        # 打开指定的网页
        driver.get(url)

        # 用集合来存储链接，确保不重复
        unique_links = set()

        while True:
            # 显式等待，等待包含链接的<div>加载完成
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "news_wz"))
            )

            # 找到所有<div class="news_wz">元素
            news_wz_divs = driver.find_elements(By.CLASS_NAME, "news_wz")

            # 遍历每个<div>，提取其中的链接
            for div in news_wz_divs:
                # 找到当前<div>下的所有链接
                hrefs = div.find_elements(By.TAG_NAME, "a")

                # 提取链接并添加到集合中
                for href in hrefs:
                    link = href.get_attribute("href")
                    print(link)
                    unique_links.add(link)

                    # 将链接写入文件
                    with open(output_file, "a") as file:
                        file.write(link + "\n")

            # 查找并模拟点击下一页按钮
            next_button = driver.find_element(By.XPATH, "//a[@class='next']")
            if next_button.is_enabled():
                driver.execute_script("arguments[0].click();", next_button)
                # 显式等待，等待新页面加载完成
                WebDriverWait(driver, 10).until(EC.staleness_of(news_wz_divs[0]))
            else:
                # 如果没有下一页，退出循环
                break

    finally:
        # 关闭浏览器
        driver.quit()


# 测试函数，将唯一的链接逐步写入到output.txt文件中
crawl_webpage_and_extract_hrefs("https://cos.njfu.edu.cn/75/list.htm")
