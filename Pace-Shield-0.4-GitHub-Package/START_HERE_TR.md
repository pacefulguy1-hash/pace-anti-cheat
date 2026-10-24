# Paceful Shield 0.4 Beta — GitHub'a aktarma rehberi

Bu ZIP, `pace-shield` adlı GitHub deposu için hazırlanmış 0.4 dosyalarını doğru klasör yollarıyla içerir. **Henüz GitHub'a gönderilmedi.** Bu oturumdaki GitHub entegrasyonu yeni dal oluşturma izni vermediği için dosyaları doğrudan depoya kaydedemedim. Aşağıdaki yöntemle kendi hesabından gönderebilirsin.

## Önce bilmen gerekenler

- Eski `app/pace_app_v03.py` ve 0.3 kurulum dosyası değiştirilmez; bu pakette yeni `app/pace_app_v04.py` ve yeni kurulum dosyası bulunur.
- `index.html`, `script.js`, `styles.css` ve `README.md` dosyaları 0.4 marka ve site tasarımı için yenileriyle değiştirilir.
- İndirme düğmesi sadece `v0.4.0-beta` GitHub Release yayımlanmış ve kurulum dosyası eklenmişse çalışır.
- 0.4 henüz Windows üzerinde bu ortamdan kurulup denenemedi; genel kullanıma açmadan önce test edilmelidir.

Depo adını GitHub üzerinde `pace-shield` yaptıktan sonra depo adresi `https://github.com/pacefulguy1-hash/pace-shield`, Pages adresi de `https://pacefulguy1-hash.github.io/pace-shield/` olur. Pages ayarlarını kontrol et.

## Önerilen yöntem: GitHub Desktop

1. Bu paket ZIP'ini indirip bir klasöre çıkart.
2. GitHub Desktop'ı aç. `File → Clone repository` seçeneğine gir ve `https://github.com/pacefulguy1-hash/pace-shield` adresini klonla.
3. GitHub Desktop'ta `Current Branch` açılır menüsünden `New Branch` seç. Dal adına `feature/paceful-shield-0.4` yazıp oluştur.
4. Klonladığın `pace-shield` klasörünü Dosya Gezgini'nde aç. ZIP'ten çıkardığın paketin **içindeki tüm dosya ve klasörleri** buraya kopyala. Sorulursa `index.html`, `script.js`, `styles.css` ve `README.md` dosyalarının değiştirilmeyi kabul et.
5. GitHub Desktop'a dön. Değişikliklerin listelendiğini kontrol et. Summary alanına `Prepare Paceful Shield 0.4 Beta` yazıp `Commit to feature/paceful-shield-0.4` düğmesine bas.
6. `Push origin` ile dalı GitHub'a gönder ve `Create Pull Request` ile değişiklikleri incelemeye aç. Eski 0.3 dosyaları yerinde kalmalı.
7. PR'ı birleştirdikten sonra GitHub deposunda `Actions → Build Paceful Shield 0.4 Windows Installer → Run workflow` yolunu açıp iş akışını çalıştır.
8. İşlem başarılı olursa `Paceful-Shield-Setup-0.4.0-beta-Windows-x64` adlı artifact'i indirip Windows'ta test et. GitHub Releases'teki 0.4 taslağını testten sonra yayımla; web sitesinin indirme düğmesi bundan sonra etkinleşir.

## Bu beta sürümünde olmayan özellik

Dosyanın işletim sistemi düzeyinde çalıştırılmasını engelleme henüz uygulanmadı. Yanlış bir AppLocker veya Software Restriction Policy kuralı diğer uygulamaları bozabileceğinden, test edilmemiş bir engelleme düğmesi eklemedim. Şüpheli dosyalar için onaylı Geri Dönüşüm Kutusu'na taşıma ve Defender'ın belirli dosyayı taramasını isteme bulunur.
