import browser, excel, mail

if __name__ == '__main__':
    usd_info = browser.get_info('usd')
    excel.write_to_excel(usd_info, 'usd')
    
    eur_info = browser.get_info('eur')
    excel.write_to_excel(eur_info, 'eur')

    excel.euro_to_dollar_ratio()

    addr_to = 'kornilovqwerty@gmail.com'
    file = [f'C:/Users/Aleksey/Desktop/test/{excel.FILE_NAME}']
    mail.send_email(addr_to, 'Курс доллара и евро', excel.number_of_lines(), file)