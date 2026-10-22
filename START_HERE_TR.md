# PACE 0.2 Beta — Şimdi yapman gerekenler

Bu ZIP, mevcut `pace-anti-cheat` GitHub deposuna eklenmek üzere hazırlanmış **dosya paketi**dir. Benim GitHub bağlantım depoya dosya yazamadığı için yüklemeyi senin hesabından yapman gerekiyor.

## A) Dosyaları depoya aktar

1. Bu ZIP'i klasöre çıkart.
2. İçindeki dosya ve klasörleri mevcut `pacefulguy1-hash/pace-anti-cheat` deposunun ana dizinine yükle; `index.html`, `script.js`, `styles.css` ve `404.html` sorulduğunda eskilerinin yerine yenilerini koy.
3. Bunlar da deponun ana dizinine eklenmeli: `_config.yml`, `.nojekyll`, `README.md`, `RELEASE_NOTES.md`, `PRIVACY.md`, `build_windows.bat`, `app/`, `installer/` ve `.github/`.
4. `.github/workflows/build-windows-installer.yml` yolunun aynen korunduğundan emin ol; bu dosyayı başka bir klasörün içinde bırakma.
5. **Commit changes** ile kaydet. Bu, yeni bir GitHub Pages derlemesini de tetikler.

## B) 404 hatasını yeniden kontrol et

- Beklenen adres: https://pacefulguy1-hash.github.io/pace-anti-cheat/
- Pages ayarı `main` ve `/(root)` olmalı.
- GitHub deposunda **Actions → pages build and deployment** işleminin tamamlanmasını bekle. Yeşil başarı görünüyorsa Summary bölümündeki **environment URL** bağlantısına tıkla; adresi kendin yeniden yazmak yerine o bağlantıyı kullan.
- Hâlâ 404 görürsen Edge'de `Ctrl+F5` ile önbelleksiz yenile ve URL'de `/pace-anti-cheat/` bölümünün bulunduğunu kontrol et.

## C) Gerçek Windows kurulum dosyasını oluştur

1. GitHub deposunda **Settings → Actions → General** bölümünü aç. Gerekirse **Workflow permissions** altında `Read and write permissions` iznini seç ve kaydet. Workflow yalnızca depodaki sürüm taslağını oluşturmak/güncellemek için içerik yazma izni ister.
2. **Actions → Build PACE Windows Installer → Run workflow** yolunu aç.
3. `Run workflow` düğmesine bas ve Windows derlemesinin tamamlanmasını bekle.
4. Yeşil başarı sonucu gelirse çalışmanın sayfasında `PACE-Setup-0.2.0-beta-Windows-x64` adlı artifact'i indir. ZIP'i çıkar ve içindeki `PACE-Setup-0.2.0-beta.exe` dosyasını kendi Windows bilgisayarında test et.
5. Workflow aynı zamanda `Releases` bölümünde `v0.2.0-beta` başlıklı bir **taslak (draft)** release oluşturur. Kurulumu test etmeden taslağı yayımlama.
6. Testten sonra GitHub'da **Releases → Draft PACE Anti-Cheat 0.2 Beta → Edit** yolunu aç ve `Publish release` ile yayımla. Site, resmî release içinde `PACE-Setup-0.2.0-beta.exe` dosyasını bulduğunda indirme düğmesi otomatik etkinleşir.

## Dürüst güvenlik notu

Kurulum dosyası GitHub Actions'ın Windows makinesinde üretilir ve SHA-256 kontrol dosyası eşlik eder. Bu beta için kod imzalama sertifikası yoktur; bu yüzden dosya imzasızdır ve SmartScreen uyarısı gösterebilir. PACE kendi antivirüs motoruna sahip değildir; Microsoft Defender durumunu okur ve tarama isteği gönderir. Dosyayı test etmeden veya sınırlarını açıklamadan geniş kitlelere dağıtma.
