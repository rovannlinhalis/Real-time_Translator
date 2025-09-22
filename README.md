# Real-time Translator

Aplicação desktop (.exe para Windows) que realiza tradução em tempo real de áudio, utilizando a API da OpenAI.  
Ideal para comunicação multilíngue instantânea em reuniões, jogos online ou transmissões ao vivo.

---

## 📌 Funcionalidades
- Tradução em tempo real de áudio de entrada para a língua desejada.
- Configuração flexível de dispositivos de entrada e saída de áudio.
- Feedback em áudio para retorno da tradução.
- Compatibilidade com dispositivos virtuais de loopback (ex.: Voicemeeter).

---

## ⚙️ Pré-requisitos
1. **Chave de API da OpenAI** (necessária para o funcionamento da tradução).  
   - Crie uma conta em [OpenAI](https://platform.openai.com/) e gere sua API Key.  

2. **Dispositivo de áudio** para entrada e saída.  
   - Pode ser microfone, placa de som ou dispositivo virtual (ex.: Voicemeeter).

---

## 🚀 Instalação
1. Baixe os arquivos `RealtimeTranslator.zip` e extraia para uma pasta de sua preferência.
2. Execute o aplicativo.
3. Informe sua **API Key** da OpenAI no campo indicado.
4. Configure:
   - **Input**: dispositivo de entrada de áudio (ex.: microfone ou loopback).
   - **Output**: dispositivo de saída de áudio.
   - **Output Language**: idioma desejado para a tradução (ex.: `en-US`, `pt-BR`).
5. Clique em **Enable Translator** para iniciar.

---

## 🎧 Configuração de Loopback com Voicemeeter (Recomendado)
Para traduzir **o áudio que toca no Windows** (vídeos, reuniões, etc.), é necessário configurar um dispositivo virtual de loopback.  
Recomendamos o uso do **Voicemeeter**:

1. Baixe e instale o [Voicemeeter Banana](https://vb-audio.com/Voicemeeter/banana.htm).
2. Nas configurações do Windows:
   - Defina **Voicemeeter Input** como dispositivo de **saída padrão**.
   - Defina **Voicemeeter AUX Output** como dispositivo de **entrada padrão**.
3. No aplicativo **Realtime Translator**:
   - Em **Input**, selecione `Voicemeeter Out B1`.
   - Em **Output**, selecione `Voicemeeter AUX Input`.
4. Habilite o tradutor e comece a reproduzir qualquer áudio no Windows — ele será capturado, traduzido e reproduzido em tempo real.

---

## 🖥️ Interface
A interface possui três seções principais:

- **Input**: configuração do dispositivo de entrada de áudio.
- **Feedback**: dispositivo de retorno (opcional).
- **Output**: idioma e dispositivo de saída de áudio da tradução.
- **Log**: exibe informações em tempo real sobre dispositivos e status da tradução.


<img width="760" height="424" alt="image" src="https://github.com/user-attachments/assets/643d9f84-4f41-4b42-8b07-1ba106a349dc" />


---

## 🔧 Exemplo de Uso
1. Reproduza um vídeo em francês no YouTube.  
2. Configure o **Input** como `Voicemeeter Out B1`.  
3. Configure o **Output Language** como `en-US`.  
4. Ative o tradutor.  
➡ O áudio será traduzido em tempo real e reproduzido em inglês.  

---

## 📄 Licença
Este projeto é de uso pessoal/experimental.  
Certifique-se de respeitar os termos de uso da [OpenAI](https://platform.openai.com/policies/terms-of-use).  

---
