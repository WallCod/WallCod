# 📊 Configuração do GitHub Stats Personalizado

Este documento explica como foi configurado o sistema de estatísticas do GitHub no perfil, incluindo acesso a repositórios privados.

## 🎯 Problema Original

Os serviços públicos de GitHub Stats (como Vercel compartilhado) não conseguem acessar dados de repositórios privados por questões de segurança. Isso resultava em:

- ❌ Linguagens de repos privados não apareciam
- ❌ Commits em repos privados não eram contabilizados
- ❌ Estatísticas incompletas

## ✅ Solução Implementada

Deploy personalizado no Render com GitHub Personal Access Token configurado.

---

## 🚀 Como Foi Feito

### 1️⃣ Fork do Repositório

1. Acessar: https://github.com/anuraghazra/github-readme-stats
2. Clicar em **Fork** (canto superior direito)
3. Criar fork no seu GitHub pessoal

### 2️⃣ Criar GitHub Personal Access Token (PAT)

1. Acessar: https://github.com/settings/tokens
2. Clicar em **Generate new token** → **Generate new token (classic)**
3. Configurar o token:
   - **Nome**: `GitHub Stats Render` (ou qualquer nome descritivo)
   - **Expiração**: Escolher período desejado (recomendado: 90 dias ou sem expiração)
   - **Escopos necessários**:
     - ✅ `repo` - Acesso completo aos repositórios privados
     - ✅ `read:user` - Ler informações do usuário
4. Clicar em **Generate token**
5. **⚠️ COPIAR E GUARDAR O TOKEN** - Você não conseguirá vê-lo novamente!

### 3️⃣ Deploy no Render

1. Acessar: https://render.com
2. Fazer login ou criar conta (plano gratuito disponível)
3. No dashboard, clicar em **New +** → **Web Service**
4. Conectar com GitHub e selecionar o repositório do fork
5. Configurações do deploy:
   ```
   Name: wall-readme-stats (ou qualquer nome)
   Region: Oregon (US West) ou região mais próxima
   Branch: master
   Runtime: Node
   Build Command: npm install
   Start Command: node express.js
   ```
6. **Environment Variables** (Variáveis de Ambiente):
   - **Key**: `PAT_1`
   - **Value**: [Cole o token criado no passo 2]
7. **Plan**: Free
8. Clicar em **Create Web Service**

### 4️⃣ Aguardar Deploy

- O Render fará o build e deploy automaticamente
- URL gerada: `https://wall-readme-stats.onrender.com`
- Primeiro deploy pode levar 2-5 minutos

### 5️⃣ Atualizar README.md

URLs atualizadas no README para usar o deploy personalizado:

```markdown
<div align="center">
  <img src="https://wall-readme-stats.onrender.com/api?username=WallCod&show_icons=true&count_private=true&include_all_commits=true&hide_border=true&title_color=FDB927&icon_color=FDB927&text_color=c9d1d9&bg_color=0d1117" alt="GitHub Stats" />

  <img src="https://wall-readme-stats.onrender.com/api/top-langs/?username=WallCod&layout=compact&hide_border=true&title_color=FDB927&text_color=c9d1d9&bg_color=0d1117&langs_count=8&count_private=true" alt="Top Languages" />
</div>
```

---

## 🎨 Parâmetros Utilizados

### GitHub Stats Card

- `username=WallCod` - Seu usuário do GitHub
- `show_icons=true` - Mostra ícones
- `count_private=true` - ✅ Conta repositórios privados
- `include_all_commits=true` - ✅ Inclui todos os commits
- `hide_border=true` - Remove borda
- `title_color=FDB927` - Cor dourada dos títulos
- `icon_color=FDB927` - Cor dourada dos ícones
- `text_color=c9d1d9` - Cor do texto
- `bg_color=0d1117` - Cor de fundo escura

### Top Languages Card

- `username=WallCod` - Seu usuário do GitHub
- `layout=compact` - Layout compacto
- `hide_border=true` - Remove borda
- `title_color=FDB927` - Cor dourada
- `text_color=c9d1d9` - Cor do texto
- `bg_color=0d1117` - Cor de fundo
- `langs_count=8` - Mostra até 8 linguagens
- `count_private=true` - ✅ Conta linguagens de repos privados

---

## ⚠️ Importante Saber

### Cold Start (Render Free Plan)

- O plano gratuito do Render "dorme" após 15 minutos de inatividade
- Primeira requisição após inatividade pode demorar 30-60 segundos
- Após "acordar", funciona normalmente
- GitHub faz cache das imagens, então visitantes não sentem o delay

### Manutenção do Token

- Tokens podem expirar conforme configurado
- Se expirar, as stats voltarão a não mostrar dados privados
- Para renovar:
  1. Criar novo token no GitHub
  2. Atualizar variável `PAT_1` no Render
  3. Reiniciar o serviço

### URLs Antigas vs Novas

**❌ URLs antigas (serviços públicos):**
- `github-readme-stats-sigma-five.vercel.app`
- `github-readme-stats.vercel.app`
- Sem acesso a repos privados

**✅ URL atual (deploy personalizado):**
- `wall-readme-stats.onrender.com`
- Com acesso completo via token

---

## 🔧 Troubleshooting

### Stats não aparecem

1. Verificar se o serviço no Render está ativo (pode estar em cold start)
2. Verificar logs no dashboard do Render
3. Confirmar que o token `PAT_1` está configurado corretamente

### Stats não mostram dados privados

1. Verificar se o token tem os escopos `repo` e `read:user`
2. Confirmar que o token não expirou
3. Verificar se a variável `count_private=true` está nas URLs

### Deploy falhou

1. Verificar logs de build no Render
2. Confirmar que o repositório fork está atualizado
3. Verificar se os comandos de build/start estão corretos

---

## 📚 Recursos

- [GitHub Readme Stats - Repositório Oficial](https://github.com/anuraghazra/github-readme-stats)
- [Render Documentação](https://render.com/docs)
- [GitHub Personal Access Tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)

---

## ✨ Resultado Final

Agora o perfil mostra:
- ✅ Todas as linguagens utilizadas (públicas + privadas)
- ✅ Total real de commits
- ✅ Estatísticas completas e precisas
- ✅ Design customizado com cores do perfil (#FDB927)

**Deploy URL:** https://wall-readme-stats.onrender.com

**Data de Configuração:** Janeiro 2026
