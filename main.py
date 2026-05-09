import requests
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def is_URL_warning(url):
    parsed = urlparse(url)
    domain = parsed.netloc.lower()
    path = parsed.path.lower()
    query = parsed.query.lower()

    warning = []

    warning_keywords = [ # подозрительные ключевые слова
        'login', 'password', 'paypal', 'account', 'update', 'bank', 'verify'
    ]

    # Проверяем есть ли подозрительные ключевые слова
    for keyword in warning_keywords:
        if keyword in domain or keyword in path or keyword in query:
            warning.append(f"Подозрительное ключевое слово: {keyword}")

    # Проверяем длину домена
    if len(domain) > 60:
        warning.append("Слишком длинный домен (>60 символов)")

    # Проверяем дефисы в домене
    if domain.count('-') > 2:
        warning.append("Много дефисов в домене")

    return warning
def get_child_links(url):
    try:
        response = requests.get(url, timeout=10, verify=True)

        soup = BeautifulSoup(response.text, 'lxml')
        links = set()
        base_domain = urlparse(url).netloc
        error_links = []

        for link in soup.find_all('a', href=True):
            href = link['href']
            absolute_url = urljoin(url, href)

            URL_warning= is_URL_warning(absolute_url)# Проверка URL
            if URL_warning:
                error_links.append(f"Проблемы в ссылке {absolute_url}: {', '.join(URL_warning)}")

            # только ссылки с того же доменаgit remote -v
            if urlparse(absolute_url).netloc == base_domain:
                links.add(absolute_url)

        return sorted(links), error_links

    except:
        print(f"Ошибка")
        return [], []

def save_analysis(links, warning, URL, filename="analysis.txt"):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("Анализ безопасности дочерних ссылок сайта \n")
        f.write("Проверяемые признаки: \n")
        f.write("# 1. Проверяем есть ли подозрительные ключевые слова \n")
        f.write("# 2. Проверяем длину домена \n")
        f.write("# 3. Проверяем дефисы в домене \n")

        f.write(f"Проверяемый URL: {URL}\n\n")


        if warning:
            f.write("Присутствуют подозрительные символы:\n")
            f.write("\n- ".join(warning) + "\n\n")
        else:
            f.write("Анализируемых подозрительных ссылок не обнаружено\n\n")

        for link in links:
            f.write(link + "\n")
        f.write(f"Найдено дочерних ссылок: {len(links)}\n")
        f.write(f"Дата анализа: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    print(f"Результаты анализа находятся в файле '{filename}'")

def main():
    print("Программа предназначена для проверки на фишинг дочерних ссылок сайта")
    URL = input("\nВведите URL сайта : ").strip()

    print(f"\nАнализ сайта: {URL}")

    links, security_issues = get_child_links(URL)
    save_analysis(links, security_issues, URL)

if __name__ == "__main__":
    main()
