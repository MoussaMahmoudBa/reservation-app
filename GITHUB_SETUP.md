# 🔐 Configuration GitHub - Authentification

## Problème d'authentification détecté

Vous devez vous authentifier avec GitHub pour pousser votre code.

## 🚀 Solutions

### **Option 1 : Token d'accès personnel (Recommandé)**

1. **Allez sur GitHub** : https://github.com/settings/tokens
2. **Cliquez** sur "Generate new token (classic)"
3. **Donnez un nom** : "Reservation App"
4. **Sélectionnez les permissions** :
   - ✅ `repo` (toutes les permissions repo)
   - ✅ `workflow` (si vous voulez utiliser GitHub Actions)
5. **Cliquez** sur "Generate token"
6. **Copiez le token** (vous ne le reverrez plus !)

### **Option 2 : Utiliser SSH (Alternative)**

1. **Générer une clé SSH** :
   ```bash
   ssh-keygen -t ed25519 -C "votre-email@example.com"
   ```

2. **Ajouter la clé à GitHub** :
   - Copiez le contenu de `~/.ssh/id_ed25519.pub`
   - Allez sur https://github.com/settings/keys
   - Cliquez sur "New SSH key"

3. **Changer l'URL du remote** :
   ```bash
   git remote set-url origin git@github.com:MoussaMahmoudBa/reservation-app.git
   ```

## 🔧 Configuration après authentification

### **Avec Token d'accès personnel :**
```bash
# Quand Git vous demande votre nom d'utilisateur et mot de passe :
# Username: MoussaMahmoudBa
# Password: [votre-token-d'accès-personnel]
```

### **Avec SSH :**
```bash
git remote set-url origin git@github.com:MoussaMahmoudBa/reservation-app.git
git push -u origin main
```

## ✅ Vérification

Après authentification, vous devriez pouvoir pousser votre code :

```bash
git push -u origin main
```

## 🎯 Prochaines étapes

Une fois le code poussé sur GitHub :

1. **Allez sur Railway** : https://railway.app/
2. **Connectez votre repository GitHub**
3. **Déployez le backend Django**

## 📞 Support

- **Documentation GitHub** : https://docs.github.com/
- **GitHub CLI** : https://cli.github.com/
- **SSH Keys** : https://docs.github.com/en/authentication/connecting-to-github-with-ssh 