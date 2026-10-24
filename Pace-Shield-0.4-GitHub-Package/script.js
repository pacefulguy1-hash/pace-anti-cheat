(() => {
  const RELEASE_API = 'https://api.github.com/repos/pacefulguy1-hash/pace-shield/releases/tags/v0.4.0-beta';
  const INSTALLER_NAME = 'Paceful-Shield-Setup-0.4.0-beta.exe';
  const translations = {
    en: {
      tagline:'WINDOWS SECURITY COMPANION',navFeatures:'Features',navHow:'How it works',navDownload:'Download',getApp:'Get the app',languageLabel:'Language',
      eyebrow:'WINDOWS SECURITY · BETA 0.4',heroTitle:'A clearer view of your PC’s security.',heroText:'Paceful Shield works alongside Microsoft Defender, watches selected folders, and helps you understand security findings without pretending every warning is a confirmed virus.',downloadWindows:'Download for Windows',seeHow:'See how it works',heroFoot:'Windows app · Clear limitations · No fake “100% protected” claims',cardMonitoring:'Folder monitoring',active:'ACTIVE',cardDefender:'Microsoft Defender',cardTogether:'Works alongside Windows security',
      trustLocal:'Local-first file review',trustChoice:'You decide what to remove',trustHonest:'Clear beta limitations',featuresKicker:'BUILT FOR CLARITY',featuresTitle:'Useful security tools. Honest status.',featuresText:'Bring everyday security checks together while keeping Microsoft Defender enabled.',
      featureStatusTitle:'Defender status',featureStatusText:'View antivirus, real-time protection, service, and security intelligence status reported by Windows.',featureWatchTitle:'Automatic folder review',featureWatchText:'Watch selected locations and periodically inspect a limited number of files for suspicious patterns.',featureAlertsTitle:'Desktop alerts',featureAlertsText:'Receive a Windows notification when a new heuristic finding or a newly reported Defender threat is observed.',featureScanTitle:'Defender scan controls',featureScanText:'Request a quick or full Microsoft Defender scan and view available Defender threat-history entries.',featureRemoveTitle:'User-approved removal',featureRemoveText:'Review the reason first. If you choose, move a flagged file to the Recycle Bin. Files are never removed automatically.',featureExcludeTitle:'Your exclusions',featureExcludeText:"Exclude a file or folder from Paceful Shield's own review without changing Microsoft Defender exclusions.",featurePerformanceTitle:'System performance',featurePerformanceText:'View CPU, memory, disk usage, and the processes using the most memory.',featureNetworkTitle:'Network overview',featureNetworkText:'Review active network connections locally. A connection is not marked malicious just because it is unfamiliar.',
      howKicker:'HOW IT WORKS',howTitle:'A helpful companion, not a replacement antivirus.',howText:'Paceful Shield uses Windows security information where available and applies a small set of local review rules. Findings are clues to investigate—not proof that a file is infected.',releaseNotes:'Read the 0.4 beta notes →',step1Title:'Choose watched folders',step1Text:'Downloads, Desktop, Documents, and folders you add.',step2Title:'Review new findings',step2Text:'Read the reason and check with Microsoft Defender.',step3Title:'You stay in control',step3Text:'Nothing is automatically deleted or quarantined.',noticeTitle:'Important beta security note',noticeText:'Paceful Shield 0.4 is experimental. It is not a full antivirus, cannot guarantee detection, does not block individual files at OS level in this beta, and cannot guarantee it will survive termination by an administrator. Keep Microsoft Defender enabled.',downloadKicker:'PACEFUL SHIELD · 0.4 BETA',downloadTitle:'Ready to review your PC security?',downloadText:'Windows x64 installer. Please test beta software carefully and keep Microsoft Defender enabled.',downloadLoading:'Checking official release…',downloadStatus:'The button activates only when the 0.4 installer is available in the official GitHub release.',githubLink:'GitHub repository ↗',notesLink:'Release notes',footerText:'Windows security companion · Beta software · Keep Defender enabled',releaseReady:'Download Paceful Shield 0.4 Beta',releaseFailed:'The 0.4 installer is not currently available in the public release. Please check again after it is published.'
    },
    tr: {
      tagline:'WINDOWS GÜVENLİK YARDIMCISI',navFeatures:'Özellikler',navHow:'Nasıl çalışır',navDownload:'İndir',getApp:'Uygulamayı edin',languageLabel:'Dil',
      eyebrow:'WINDOWS GÜVENLİĞİ · BETA 0.4',heroTitle:'Bilgisayarının güvenliğini daha net gör.',heroText:'Paceful Shield, Microsoft Defender ile birlikte çalışır, seçtiğin klasörleri izler ve her uyarıyı doğrulanmış virüs gibi göstermeden güvenlik bulgularını anlamana yardımcı olur.',downloadWindows:'Windows için indir',seeHow:'Nasıl çalışır?',heroFoot:'Windows uygulaması · Açık sınırlamalar · Sahte “%100 koruma” iddiaları yok',cardMonitoring:'Klasör izleme',active:'ETKİN',cardDefender:'Microsoft Defender',cardTogether:'Windows güvenliğiyle birlikte çalışır',
      trustLocal:'Öncelikle yerel dosya incelemesi',trustChoice:'Neyi kaldıracağına sen karar verirsin',trustHonest:'Açık beta sınırlamaları',featuresKicker:'ANLAŞILIR GÜVENLİK',featuresTitle:'İşe yarayan araçlar. Dürüst durum bilgisi.',featuresText:'Microsoft Defender açık kalırken günlük güvenlik kontrollerini tek yerde birleştir.',
      featureStatusTitle:'Defender durumu',featureStatusText:'Windows tarafından bildirilen antivirüs, gerçek zamanlı koruma, hizmet ve güvenlik imzası durumunu görüntüle.',featureWatchTitle:'Otomatik klasör incelemesi',featureWatchText:'Seçtiğin konumları izle ve belirli aralıklarla sınırlı sayıda dosyada şüpheli örüntüleri incele.',featureAlertsTitle:'Masaüstü bildirimleri',featureAlertsText:'Yeni bir kural bulgusu veya Defender tarafından bildirilen yeni bir tehdit görüldüğünde Windows bildirimi al.',featureScanTitle:'Defender tarama kontrolleri',featureScanText:'Microsoft Defender hızlı veya tam taraması başlatma isteği gönder ve Defender tehdit geçmişini görüntüle.',featureRemoveTitle:'Onaylı kaldırma',featureRemoveText:'Önce nedeni incele. Sen seçersen işaretlenen dosyayı Geri Dönüşüm Kutusu’na taşı. Dosyalar otomatik silinmez.',featureExcludeTitle:'İstisnaların',featureExcludeText:'Microsoft Defender istisnalarını değiştirmeden, dosya veya klasörü yalnızca Paceful Shield incelemesinden hariç tut.',featurePerformanceTitle:'Sistem performansı',featurePerformanceText:'İşlemci, bellek ve disk kullanımını; en çok bellek tüketen işlemlerle birlikte görüntüle.',featureNetworkTitle:'Ağ görünümü',featureNetworkText:'Aktif ağ bağlantılarını yerel olarak incele. Bilinmeyen bir bağlantı tek başına zararlı olduğu anlamına gelmez.',
      howKicker:'NASIL ÇALIŞIR',howTitle:'Antivirüsün yerine değil, yanında çalışan yardımcı.',howText:'Paceful Shield, erişilebildiğinde Windows güvenlik bilgilerini kullanır ve az sayıda yerel inceleme kuralı uygular. Bulgular araştırılması gereken işaretlerdir; dosyanın virüslü olduğunun kanıtı değildir.',releaseNotes:'0.4 beta notlarını oku →',step1Title:'İzlenecek klasörleri seç',step1Text:'İndirilenler, Masaüstü, Belgeler ve senin eklediklerin.',step2Title:'Yeni bulguları incele',step2Text:'Neden işaretlendiğini oku ve Microsoft Defender ile kontrol et.',step3Title:'Kontrol sende',step3Text:'Hiçbir dosya otomatik silinmez veya karantinaya alınmaz.',noticeTitle:'Önemli beta güvenlik notu',noticeText:'Paceful Shield 0.4 deneyseldir. Tam bir antivirüs değildir, her tehdidi bulmayı garanti etmez, bu beta sürümünde dosyaların çalıştırılmasını işletim sistemi düzeyinde engellemez ve yönetici tarafından sonlandırılmaya karşı koruma garantisi vermez. Microsoft Defender açık kalsın.',downloadKicker:'PACEFUL SHIELD · BETA 0.4',downloadTitle:'Bilgisayarının güvenliğini incelemeye hazır mısın?',downloadText:'Windows x64 kurulum dosyası. Beta yazılımını dikkatle test et ve Microsoft Defender’ı açık tut.',downloadLoading:'Resmî sürüm kontrol ediliyor…',downloadStatus:'İndirme düğmesi yalnızca 0.4 kurulum dosyası resmî GitHub sürümünde yayımlandığında etkinleşir.',githubLink:'GitHub deposu ↗',notesLink:'Sürüm notları',footerText:'Windows güvenlik yardımcısı · Beta yazılımı · Defender açık kalsın',releaseReady:'Paceful Shield 0.4 Beta’yı indir',releaseFailed:'0.4 kurulum dosyası şu anda herkese açık sürümde bulunamadı. Yayımlandıktan sonra yeniden kontrol et.'
    }
  };
  const root = document.documentElement;
  const languageSelect = document.getElementById('language-select');
  const themeToggle = document.getElementById('theme-toggle');
  const downloadButton = document.getElementById('download-button');
  const heroDownload = document.getElementById('hero-download');
  const downloadStatus = document.getElementById('download-status');
  document.getElementById('year').textContent = String(new Date().getFullYear());

  function setLanguage(language) {
    const dict = translations[language] || translations.en;
    root.lang = language;
    document.querySelectorAll('[data-i18n]').forEach(node => {
      const key = node.getAttribute('data-i18n');
      if (dict[key]) node.textContent = dict[key];
    });
    languageSelect.value = language;
    try { localStorage.setItem('pacefulshield-language', language); } catch (_) {}
  }
  function setTheme(theme) {
    root.dataset.theme = theme;
    themeToggle.textContent = theme === 'light' ? '☾' : '☼';
    themeToggle.setAttribute('aria-label', theme === 'light' ? 'Switch to dark theme' : 'Switch to light theme');
    try { localStorage.setItem('pacefulshield-theme', theme); } catch (_) {}
  }
  function setDownloadReady(url) {
    downloadButton.href = url;
    downloadButton.classList.remove('disabled');
    downloadButton.removeAttribute('aria-disabled');
    downloadButton.textContent = translations[root.lang].releaseReady;
    heroDownload.href = url;
    downloadStatus.textContent = INSTALLER_NAME;
  }
  async function loadRelease() {
    try {
      const response = await fetch(RELEASE_API, {headers: {'Accept': 'application/vnd.github+json'}});
      if (!response.ok) throw new Error('Release not found or unpublished');
      const release = await response.json();
      const asset = (release.assets || []).find(item => item.name === INSTALLER_NAME && item.state !== 'starter');
      if (!asset || !asset.browser_download_url || release.draft) throw new Error('Installer not published');
      setDownloadReady(asset.browser_download_url);
    } catch (_) {
      downloadButton.classList.add('disabled');
      downloadButton.setAttribute('aria-disabled', 'true');
      downloadButton.href = '#download';
      downloadButton.textContent = translations[root.lang].downloadLoading;
      heroDownload.href = '#download';
      downloadStatus.textContent = translations[root.lang].releaseFailed;
    }
  }
  languageSelect.addEventListener('change', () => { setLanguage(languageSelect.value); });
  themeToggle.addEventListener('click', () => setTheme(root.dataset.theme === 'light' ? 'dark' : 'light'));
  const savedLanguage = (() => { try { return localStorage.getItem('pacefulshield-language'); } catch (_) { return null; } })();
  const savedTheme = (() => { try { return localStorage.getItem('pacefulshield-theme'); } catch (_) { return null; } })();
  setLanguage(savedLanguage && translations[savedLanguage] ? savedLanguage : 'en');
  setTheme(savedTheme === 'light' ? 'light' : 'dark');
  loadRelease();
})();
