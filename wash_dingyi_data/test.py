import re


main_industry = '366901 Emergency alarms'
result = re.sub(r'\D*', '', main_industry)
print(result)


def main(i):
    print(i)


for i in range(0, 5):
    main(i)


print('fefefge   '.strip())