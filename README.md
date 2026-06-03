Artigo SIGH - Código de Monitoramento de Umidade com conexão MQTT
Descrição

Este projeto utiliza um microcontrolador ESP32 para monitorar a umidade através de um sensor de umidade, porém como o simulador Wowki não tinha o sensor usei um potenciômetro para simular o sensor. Os dados de umidade são enviados via MQTT para o broker test.mosquitto.org, permitindo o monitoramento remoto da umidade. O projeto também inclui um display LCD I2C para exibir informações locais sobre a conexão WiFi e MQTT.
Componentes Utilizados

    ESP32: Microcontrolador responsável por processar os dados.
    Potenciômetro (Wokwi-Potentiometer): Sensor utilizado para simular valores de umidade.
    Valvula Controlada por GPIO: Simulando um dispositivo que pode ser controlado com base nos valores de umidade.
    Display LCD I2C: Exibe informações locais sobre o estado da conexão WiFi e MQTT.

Configurações Iniciais
Conexões Hardware

    Potenciômetro:
        Ligado ao pino ADC34 do ESP32.

    Valvula (GPIO):
        Controlada pelo pino GPIO5 do ESP32.

    Display LCD I2C:
        SCL ligado ao pino GPIO22.
        SDA ligado ao pino GPIO21.

Configurações de Rede

    SSID: Wokwi-GUEST
    Senha: Deixe em branco ("") se não houver senha.

Configurações MQTT

    Broker: test.mosquitto.org (broker público para testes).
    Client ID: Gerado dinamicamente com um timestamp.
    Topicos:
        Umidade: mackenzie/luizferreira/projeto2026/umidade
        Comando: mackenzie/luizferreira/projeto2026/comando
        Status: mackenzie/luizferreira/projeto2026/status

Funcionalidades

    Leitura do Potenciômetro:
        O valor lido pelo potenciômetro é mapeado para uma escala de 0 a 100, onde 0 representa o lado esquerdo e 100 o lado direito.

    Conexão WiFi:
        O dispositivo se conecta à rede WiFi especificada.
        Informações sobre a conexão são exibidas no display LCD I2C.

    Publicação MQTT:
        Os valores de umidade lidos pelo potenciômetro são publicados no tópico mackenzie/luizferreira/projeto2026/umidade.
        O status do dispositivo é publicado no tópico mackenzie/luizferreira/projeto2026/status com o payload ONLINE.

    Recepção de Comandos MQTT:
        O dispositivo pode receber comandos no tópico mackenzie/luizferreira/projeto2026/comando.
        Comandos disponíveis:
            ON: Liga a valvula (ativa o GPIO5).
            OFF: Desliga a valvula (desativa o GPIO5).

Como Executar

    Instalar Dependências:
        Certifique-se de ter as bibliotecas necessárias instaladas no seu ambiente de desenvolvimento para ESP32, como PubSubClient para MQTT.

    Configurar WiFi:
        Altere o SSID e a senha na seção de configurações do código conforme necessário.

    Carregar o Código:
        Use uma IDE compatível com ESP32 (como Arduino IDE) para carregar o código no microcontrolador.

    Monitorar MQTT:
        Utilize um cliente MQTT para monitorar os tópicos mackenzie/luizferreira/projeto2026/umidade e mackenzie/luizferreira/projeto2026/status.
        Enviar comandos via MQTT no tópico mackenzie/luizferreira/projeto2026/comando.

Exemplos de Uso

    Monitorar a Umidade:
        Gire o potenciômetro para variar os valores de umidade.
        Os valores atualizados serão exibidos no display LCD I2C e enviados via MQTT.

    Controlar a Valvula:
        Publique um comando ON no tópico mackenzie/luizferreira/projeto2026/comando.
        A valvula será ativada (GPIO5 alto).
        Publique um comando OFF para desativar a valvula.

Contribuições

Contribuições são bem-vindas! Abra uma issue ou faça um pull request com suas sugestões e melhorias.
