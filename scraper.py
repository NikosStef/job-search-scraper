import requests
import pandas as pd
from bs4 import BeautifulSoup


def main():

    df = pd.DataFrame(columns=['title', 'company', 'location', 'salary', 'date', 'link'])

    for page in range(5):

        url = "https://www.indeed.co.uk/jobs?q=junior+data+engineer&l=London%2C+Greater+London&start={}".format(page*10)
        page = requests.get(url)

        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find(id='resultsCol')

        # add string='' for specific job
        # lambda text: 'python' in text.lower())
        job_elems = results.find_all('div', class_='jobsearch-SerpJobCard')
        for job in job_elems:
            title = job.find('div', class_='title')
            company = job.find('span', class_='company')
            location = job.find('div', class_='location')
            date = job.find('span', class_='date')
            salary = job.find('div', class_='salarySnippet')
            link = 'www.indeed.co.uk' + job.find('a')['href']

            for value in (title, company, location, salary):
                if value is None:
                    continue
                else:
                    print(value.text.strip())

            print('Posted {}'.format(date.text.strip()))
            print()

            jobs = {'title' : title, 'company' : company, 'location' : location, 'salary' : salary, 'date' : date}
            for key in jobs:
                if (jobs[key]) is None:
                    continue
                else:
                    jobs[key] = jobs[key].text.strip()
            jobs["link"]  = link
            df = df.append(jobs, ignore_index=True)

        df.to_csv('jobs.csv', index=False)


if __name__=="__main__":
    main()
