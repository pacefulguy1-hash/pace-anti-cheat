# PACE 0.3 Beta — ek dosyalar ve kurulum (Türkçe)

Bu paket mevcut PACE 0.2 dosyalarını silmez veya değiştirmez. İçindeki dosyaları aynı adlı yeni dosyalar olarak depoya eklersin; eski dosyaların üzerine yazma.

## 1) Depoya eklenecek dosyalar

ZIP içeriğini repo kök dizinine çıkar:
- `app/pace_app_v03.py`
- `installer/PACE-Setup-0.3.0-beta.iss`
- `.github/workflows/build-windows-installer-v03.yml`
- `PACE-0.3.0-BETA-NOTES.md`

Mevcut `app/assets/pace.ico` dosyası kullanılacak; bu dosya eski depoda bulunmalı. ZIP içindeki dosyalar yeni adlara sahip olduğundan 0.2 uygulama kaynağının üstüne yazmaz.

## 2) Windows kurulum dosyasını oluştur

1. GitHub deposunda **Add file → Upload files** seç.
2. Dosyaları doğru klasör yollarıyla ekle. `.github/workflows` klasöründeki YAML dosyasını da eklediğinden emin ol.
3. **Commit changes** ile kaydet.
4. **Actions** sekmesini aç.
5. Sol listeden **Build PACE 0.3 Windows Installer** seç.
6. **Run workflow → Run workflow** ile çalıştır.
7. Başarılı olunca `PACE-Setup-0.3.0-beta-Windows-x64` Artifact dosyasını indirebilirsin. Draft release da oluşturulur; herkese yayınlamadan önce sen yayımlarsın.

## 3) Kod imzalama (isteğe bağlı, sertifika gerektirir)

İmzalama için güvenilir bir sağlayıcıdan alınmış kod imzalama sertifikası gerekir. Kendi kendine imzalanan test sertifikası, başkalarının bilgisayarında yayımlayıcı güveni oluşturmaz. PFX özel anahtarını GitHub'a düz dosya olarak ekleme.

GitHub repo → Settings → Secrets and variables → Actions → New repository secret bölümünde:
- `PACE_CODESIGN_PFX_BASE64`: PFX dosyasının Base64 metni
- `PACE_CODESIGN_PASSWORD`: PFX parolası

Workflow bu iki secret ikisi de varsa hem uygulamayı hem kurulum dosyasını imzalamayı dener. Yoksa sürümü imzasız beta olarak üretir. Sertifikanın kimliğinin ve kod imzalama amacının güvenilir sağlayıcı tarafından doğrulanmış olması gerekir. Secret'ları hiç kimseyle paylaşma.

## Önemli güvenlik açıklaması

Yerel motor, seçilen klasörde sınırlı sayıdaki şüpheli örüntüleri ve zararsız EICAR test imzasını arar; bu, profesyonel antivirüs değildir. Otomatik silme/karantina yapmaz. Microsoft Defender'ı açık tut ve önemli sonuçları Windows Güvenliği'nde doğrula. PACE, Görev Yöneticisi'nden sonlandırmayı engellemez; bilgisayar sahibi uygulamayı kapatabilmelidir.
