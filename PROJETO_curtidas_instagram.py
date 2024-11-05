from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as condicao_esperada
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException
from time import sleep

def iniciar_driver():
    chrome_options = Options()
    arguments = ['--lang=pt-BR', '--window-size=1200,800', '--incognito']
    for argument in arguments:
        chrome_options.add_argument(argument)

    chrome_options.add_experimental_option('prefs', {
        'download.prompt_for_download': False,
        'profile.default_content_setting_values.notifications': 2,
        'profile.default_content_setting_values.automatic_downloads': 1,
    })

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

    wait = WebDriverWait(driver, 10, poll_frequency=1, ignored_exceptions=[NoSuchElementException])

    return driver, wait

driver, wait = iniciar_driver()

# 1. Acessar o site do Instagram
driver.get('https://instagram.com')

# 2. Encontrar campos usuário e senha, colocar valores e clicar no botão "Entrar"
campo_email = wait.until(condicao_esperada.element_to_be_clickable((By.XPATH, "//input[@name='username']")))
campo_email.send_keys('usuario_instagram')
sleep(2)
campo_senha = wait.until(condicao_esperada.element_to_be_clickable((By.XPATH, "//input[@name='password']")))
campo_senha.send_keys('senha')
sleep(3)
botao_entrar = wait.until(condicao_esperada.visibility_of_all_elements_located((By.XPATH, "//div[@class='x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh x1xmf6yo x1e56ztr x540dpk x1m39q7l x1n2onr6 x1plvlek xryxfnj x1c4vz4f x2lah0s xdt5ytf xqjyukv x1qjc9v5 x1oa3qoh x1nhvcw1']")))
botao_entrar[0].click()
sleep(5)

# 3. Fechar a janela que abre "Salvar suas informações de login"
""" try:
    fechar_informacoes_login = wait.until(condicao_esperada.element_to_be_clickable((By.XPATH, "//div[@class='x1i10hfl xjqpnuy xa49m3k xqeqjp1 x2hbi6w xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1q0g3np x1lku1pv x1a2a7pz x6s0dn4 xjyslct x1ejq31n xd10rxx x1sy0etr x17r0tee x9f619 x1ypdohk x1f6kntn xwhw2v2 xl56j7k x17ydfre x2b8uid xlyipyv x87ps6o x14atkfc xcdnw81 x1i0vuye xjbqb8w xm3z3ea x1x8b98j x131883w x16mih1h x972fbf xcfux6l x1qhh985 xm0m39n xt0psk2 xt7dq6l xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x1n5bzlp x173jzuc x1yc6y37']")))
    fechar_informacoes_login.click()
except TimeoutException:
    print("Popup de salvar login não apareceu")

# 4. Encontrar o botão "Pesquisa" e digitar o nome da página que deseja curtir as postagens
chain = ActionChains(driver)
pesquisar = wait.until(condicao_esperada.visibility_of_any_elements_located((By.XPATH, "//div[@class='x9f619 x3nfvp2 xr9ek0c xjpr12u xo237n4 x6pnmvc x7nr27j x12dmmrz xz9dl7a xn6708d xsag5q8 x1ye3gou x80pfx3 x159b3zp x1dn74xm xif99yt x172qv1o x10djquj x1lhsz42 xzauu7c xdoji71 x1dejxi8 x9k3k5o xs3sg5q x11hdxyr x12ldp4w x1wj20lx x1lq5wgf xgqcy7u x30kzoy x9jhf4c']")))

# 5. Clicar na página que deseja curtir as postagens
chain.click(pesquisar[2]).pause(2).send_keys('cristiano').pause(2).send_keys(Keys.TAB).pause(2).send_keys(Keys.TAB).pause(2).send_keys(Keys.ENTER).pause(2).perform()
sleep(3) """
driver.get('https:instagram.com/cristiano')
sleep(3)
while True:
    try:
        postagens = wait.until(condicao_esperada.visibility_of_all_elements_located((By.XPATH, "//div[@class='_aagu']")))
        print("Postagens encontradas:", len(postagens))
        sleep(4)
        # Rolar a página até a postagem
        driver.execute_script("arguments[0].scrollIntoView(true);", postagens[0])
        sleep(1)
        # 6. Abrir a última postagem e verificar se está curtida ou não
        try:
            postagens[0].click()
            print("Postagem aberta")
        except ElementClickInterceptedException:
            print("Elemento não clicável, tentando novamente")
            driver.execute_script("arguments[0].click();", postagens[0])

        sleep(4)

        #Verificar se a postagem foi curtida
        try:
            descurtir_button = driver.find_element(By.XPATH, '//section//*[@aria-label="Descurtir"]')
            print("Já foi curtido")
            # Aguarde 24 horas antes de continuar a verificação
            print("Aguardando 24 horas antes de verificar novamente")
            sleep(86400)  # 86400 segundos = 24 horas
        except NoSuchElementException:
            # Se não encontrar o botão "Descurtir", tentar encontrar o botão "Curtir" e clicar nele
            try:
                curtir_button = driver.find_element(By.XPATH, '//section//*[@aria-label="Curtir"]')
                curtir_button.click()
                print("O curtir foi clicado agora")
            except NoSuchElementException:
                print("Botão 'Curtir' não encontrado")
            except Exception as e:
                print("Erro ao clicar no botão 'Curtir':", e)

        # Fechar a postagem para continuar o loop
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
        sleep(2) 

    except TimeoutException:
        print("Nenhuma postagem encontrada ou tempo esgotado")
        break

# Fechar o driver após a execução
driver.quit()
