# 🔌 Configuration des Serveurs MCP

## Qu'est-ce que MCP ?

**MCP (Model Context Protocol)** permet à Claude Code de se connecter à des serveurs externes pour accéder à des données et services additionnels.

---

## 📦 Serveurs MCP Utiles pour ce Projet

### 1. **Serveur Filesystem** (Accès fichiers)
Permet à Claude d'accéder directement aux fichiers de votre projet.

### 2. **Serveur GitHub** (Intégration Git)
Permet de pusher/pull du code vers GitHub.

### 3. **Serveur PostgreSQL** (Base de données)
Pour sauvegarder les simulations.

### 4. **Serveur Web Search** (Recherche web)
Pour chercher de la documentation thermodynamique.

---

## ⚙️ Configuration dans Claude Code

### Étape 1 : Ouvrir les Paramètres MCP

1. Ouvrez Claude Code
2. Appuyez sur `Ctrl+Shift+P` (Windows/Linux) ou `Cmd+Shift+P` (Mac)
3. Tapez `MCP: Edit Configuration`
4. Le fichier `claude_desktop_config.json` s'ouvre

### Étape 2 : Ajouter les Serveurs

Copiez cette configuration dans votre fichier :

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "D:\\pic\\S5\\simulation et modelisation\\project python\\dist-multi-PIC11-main\\dist-multi-PIC11-main"
      ]
    },
    "github": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-github"
      ],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "VOTRE_TOKEN_GITHUB"
      }
    },
    "postgres": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-postgres",
        "postgresql://user:password@localhost:5432/distillation_db"
      ]
    }
  }
}
```

### Étape 3 : Redémarrer Claude Code

Fermez et relancez Claude Code pour activer les serveurs.

---

## 🔧 Configuration Détaillée

### 1. Serveur Filesystem

```json
{
  "filesystem": {
    "command": "npx",
    "args": [
      "-y",
      "@modelcontextprotocol/server-filesystem",
      "CHEMIN_VERS_VOTRE_PROJET"
    ]
  }
}
```

**Remplacez** `CHEMIN_VERS_VOTRE_PROJET` par le chemin absolu de votre projet.

**Capacités** :
- ✅ Lire des fichiers
- ✅ Écrire des fichiers
- ✅ Lister des répertoires
- ✅ Créer/Supprimer des fichiers

### 2. Serveur GitHub

#### 2.1 Créer un Token GitHub

1. Allez sur https://github.com/settings/tokens
2. Cliquez "Generate new token (classic)"
3. Nom : `Claude Code MCP`
4. Scopes à cocher :
   - ✅ `repo` (accès complet aux repos)
   - ✅ `workflow` (gestion workflows)
5. Cliquez "Generate token"
6. **COPIEZ LE TOKEN** (vous ne le reverrez plus !)

#### 2.2 Configuration

```json
{
  "github": {
    "command": "npx",
    "args": [
      "-y",
      "@modelcontextprotocol/server-github"
    ],
    "env": {
      "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_VOTRE_TOKEN_ICI"
    }
  }
}
```

**Capacités** :
- ✅ Créer des repositories
- ✅ Push/Pull du code
- ✅ Créer des Pull Requests
- ✅ Gérer les Issues

### 3. Serveur PostgreSQL (Optionnel)

#### 3.1 Installer PostgreSQL

**Windows** :
```bash
# Téléchargez depuis postgresql.org
# Ou avec chocolatey
choco install postgresql
```

**Linux** :
```bash
sudo apt install postgresql postgresql-contrib
```

#### 3.2 Créer la Base de Données

```bash
# Se connecter à PostgreSQL
psql -U postgres

# Créer la DB
CREATE DATABASE distillation_db;

# Créer un utilisateur
CREATE USER distillation_user WITH PASSWORD 'votre_password';

# Donner les permissions
GRANT ALL PRIVILEGES ON DATABASE distillation_db TO distillation_user;
```

#### 3.3 Configuration MCP

```json
{
  "postgres": {
    "command": "npx",
    "args": [
      "-y",
      "@modelcontextprotocol/server-postgres",
      "postgresql://distillation_user:votre_password@localhost:5432/distillation_db"
    ]
  }
}
```

**Capacités** :
- ✅ Sauvegarder les simulations
- ✅ Historique des calculs
- ✅ Comparaison de résultats

---

## 📊 Serveur Custom pour l'Application

Vous pouvez créer un serveur MCP personnalisé pour votre API de distillation !

### server-distillation.js

```javascript
#!/usr/bin/env node

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import axios from "axios";

const API_URL = process.env.DISTILLATION_API_URL || "http://localhost:5000/api";

const server = new Server(
  {
    name: "distillation-simulator",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// Tool: Lancer une simulation
server.setRequestHandler("tools/call", async (request) => {
  if (request.params.name === "simulate_distillation") {
    const { compounds, compositions, flow_rate, pressure } = request.params.arguments;

    try {
      const response = await axios.post(`${API_URL}/simulate`, {
        compounds,
        compositions,
        flow_rate,
        pressure,
        recovery_lk: 0.95,
        recovery_hk: 0.95,
        reflux_factor: 1.3,
        feed_quality: 1.0,
        efficiency: 0.70
      });

      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(response.data.results, null, 2)
          }
        ]
      };
    } catch (error) {
      return {
        content: [
          {
            type: "text",
            text: `Erreur: ${error.message}`
          }
        ],
        isError: true
      };
    }
  }
});

// Tool: Liste des composés
server.setRequestHandler("tools/list", async () => {
  return {
    tools: [
      {
        name: "simulate_distillation",
        description: "Lance une simulation de distillation multicomposants",
        inputSchema: {
          type: "object",
          properties: {
            compounds: {
              type: "array",
              items: { type: "string" },
              description: "Liste des composés (ex: ['benzene', 'toluene'])"
            },
            compositions: {
              type: "array",
              items: { type: "number" },
              description: "Compositions molaires (somme = 1.0)"
            },
            flow_rate: {
              type: "number",
              description: "Débit d'alimentation (kmol/h)"
            },
            pressure: {
              type: "number",
              description: "Pression (Pa)"
            }
          },
          required: ["compounds", "compositions", "flow_rate"]
        }
      }
    ]
  };
});

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main();
```

### Configuration dans Claude Code

```json
{
  "distillation": {
    "command": "node",
    "args": ["server-distillation.js"],
    "env": {
      "DISTILLATION_API_URL": "http://localhost:5000/api"
    }
  }
}
```

---

## 🎯 Utilisation des Serveurs MCP

Une fois configurés, vous pouvez demander à Claude :

### Avec Filesystem
```
"Lis le fichier backend/app.py et analyse les endpoints"
```

### Avec GitHub
```
"Crée un nouveau repository et push ce code"
```

### Avec PostgreSQL
```
"Sauvegarde les résultats de simulation dans la base"
```

### Avec Distillation Custom
```
"Lance une simulation BTX avec 100 kmol/h"
```

---

## ✅ Vérifier les Serveurs

### Dans Claude Code

1. Ouvrez la Command Palette (`Ctrl+Shift+P`)
2. Tapez `MCP: Show Server Status`
3. Vous verrez la liste des serveurs actifs

### Test Manual

```bash
# Test serveur filesystem
npx -y @modelcontextprotocol/server-filesystem "D:\\votre\\projet"

# Test serveur GitHub
npx -y @modelcontextprotocol/server-github
```

---

## 🐛 Dépannage

### Serveur ne démarre pas

**Solution** :
- Vérifiez que Node.js est installé : `node --version`
- Vérifiez le chemin dans la config
- Regardez les logs Claude Code

### Token GitHub invalide

**Solution** :
- Régénérez le token
- Vérifiez les scopes
- Utilisez `ghp_` au début du token

### PostgreSQL ne se connecte pas

**Solution** :
```bash
# Vérifiez que PostgreSQL tourne
pg_isready

# Testez la connexion
psql -U distillation_user -d distillation_db
```

---

## 📚 Ressources

- **MCP Documentation** : https://modelcontextprotocol.io/docs
- **MCP Servers** : https://github.com/modelcontextprotocol/servers
- **Claude Code Docs** : https://docs.anthropic.com/claude-code

---

## 🎉 Conclusion

Les serveurs MCP permettent à Claude Code de :
- ✅ Accéder à vos fichiers
- ✅ Interagir avec GitHub
- ✅ Utiliser une base de données
- ✅ Appeler votre API de distillation

**C'est comme donner des super-pouvoirs à Claude ! 🚀**

---

**Bon développement avec MCP ! 🔌✨**
