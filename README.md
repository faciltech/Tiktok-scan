<p align="center">
  <img src="https://github.com/faciltech/scan-user/assets/3409713/d5c035b9-f723-426a-856b-a472bbfe737d">
</p>
<h1 align="center">
  Tiktok-scan - Ferramenta para enumeraçao contas do Tiktok.
</h1>
<h2>🧠 Principais Funcionalidades</h2>

✔️ Consulta de perfil público
A ferramenta acessa a página de um usuário do TikTok e extrai os dados disponíveis publicamente.

✔️ Coleta de dados de usuário, incluindo:
<ul>
  <li>URL da foto de perfil</li>
  <li>ID da conta e uniqueId</li>
  <li>Nome do usuário e apelido (nickname)</li>
  <li>Biografia (bio)</li>
  <li>País/região e linguagem da conta</li>
  <li>Quantidade total de seguidores, seguindo, vídeos e corações (likes)</li>
</ul>
✔️ Levantamento de vídeos recentes, mostrando para cada vídeo:
<ul>
 <li>Descrição</li>
 <li>URL pública</li>
 <li>Métricas (visualizações, likes, comentários e compartilhamentos)</li>
</ul>
✔️ Exportação de dados
<ul>
 <li>Os dados extraídos são salvos em arquivos:</li>
  <ul>
   <li>JSON com informações gerais do perfil</li>
   <li>CSV com métricas dos vídeos recentes</li>
  </li>
  </ul>
</ul>

<h2>🛠️ Como funciona por baixo dos panos</h2>

A ferramenta faz:

Requisição HTTP ao perfil do TikTok usando o requests.

Parsing do HTML com BeautifulSoup para encontrar dados estruturados JSON no script interno da página.

Converte esse JSON em informações legíveis e práticas para OSINT ou análise básica de perfil público.

<h2>📌 Por que usar?</h2>

👉 Se você precisa verificar rapidamente informações públicas de um perfil do TikTok sem depender de APIs oficiais ou interfaces web manuais, essa ferramenta automatiza e formata esses dados para você.

⚠️ Requisitos e Observações

✔️ Requer Python instalado no sistema.
✔️ Funciona apenas com perfis públicos (contas privadas ou bloqueadas não retornam dados completos).
<h2>Como instalar </h2>

    Navegue dentro de seu sistema, escolha o local e execute no terminal o comando abaixo.

    ``` 
        git clone https://github.com/faciltech/Tiktok-scan.git
        Cloning into 'Tiktok'...
        remote: Enumerating objects: 10, done.
        remote: Counting objects: 100% (10/10), done.
        remote: Compressing objects: 100% (10/10), done.
        remote: Total 10 (delta 1), reused 0 (delta 0), pack-reused 0
        Receiving objects: 100% (10/10), 19.14 KiB | 612.00 KiB/s, done.
        Resolving deltas: 100% (1/1), done.
      ```

<h3>Conceda permissão para o arquivo!</h3>

```
chmod +x Tiktok-scan.sh
```   

<img width="1782" height="326" alt="image" src="https://github.com/user-attachments/assets/ee333dac-6915-45b5-9b0f-bbcc841187d5" />


<img width="2890" height="1312" alt="image" src="https://github.com/user-attachments/assets/2b3edb6f-fa59-4d46-9c2e-45d138cf5900" />



## 🎓 Linguagem

O utilitário é desenvolvido em linguagem python.

<!-- AUTO-GENERATED-CONTENT:END -->


