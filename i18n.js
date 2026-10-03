/**
 * NullVPN i18n — zero-dependency static language switcher
 * Supports: en, ru, fa (Farsi/RTL), ar (Arabic/RTL), es (Spanish), ne (Nepali), fr (French)
 */
(function () {
  const STORAGE_KEY = 'nullvpn_lang';
  const DEFAULT_LANG = 'en';
  const RTL_LANGS = ['fa', 'ar'];

  const LANGS = {
    en: { label: 'EN', name: 'English', flag: '🇬🇧' },
    ru: { label: 'RU', name: 'Русский', flag: '🇷🇺' },
    fa: { label: 'FA', name: 'فارسی', flag: '🇮🇷' },
    ar: { label: 'AR', name: 'العربية', flag: '🇸🇦' },
    es: { label: 'ES', name: 'Español', flag: '🇪🇸' },
    ne: { label: 'NE', name: 'नेपाली', flag: '🇳🇵' },
    fr: { label: 'FR', name: 'Français', flag: '🇫🇷' }
  };

  // ─────────────────────────────────────────────────────────────────────────────
  // TRANSLATIONS  (key → {en, ru, fa, ar, es, ne, fr})
  // ─────────────────────────────────────────────────────────────────────────────
const T = {
  "faq.h1": {
    en: "Frequently Asked Questions",
    ru: "Частые вопросы",
    fa: "سوالات متداول",
    ar: "الأسئلة الشائعة",
    es: "Preguntas frecuentes",
    ne: "बारम्बार सोधिने प्रश्नहरू",
    fr: "Foire aux questions",
  },
  "faq.sub": {
    en: "Everything you need to know before getting started.",
    ru: "Всё, что нужно знать перед началом.",
    fa: "همه چیزهایی که قبل از شروع نیاز دارید.",
    ar: "كل ما تحتاج معرفته قبل البدء.",
    es: "Todo lo que necesitas saber antes de empezar.",
    ne: "सुरु गर्नुअघि तपाईंलाई थाहा छुट्टै गर्नुपर्ने सबै कुरा।",
    fr: "Tout ce qu'il faut savoir avant de commencer.",
  },
  "how.unblock.h": {
    en: "Built for difficult networks",
    ru: "Создан для сложных сетей",
    fa: "ساخته‌شده برای شبکه‌های دشوار",
    ar: "مصمّم للشبكات الصعبة",
    es: "Diseñado para redes difíciles",
    ne: "कठिन नेटवर्कका लागि बनाइएको",
    fr: "Conçu pour les réseaux difficiles",
  },
  "how.unblock.lead": {
    en: "Traditional VPNs put many users behind one shared endpoint, which makes them crowded and inconsistent. NullVPN takes a fundamentally different approach: a private tunnel that belongs to you alone.",
    ru: "Традиционные VPN ставят множество пользователей за одну общую точку — отсюда перегрузка и нестабильность. NullVPN подходит иначе: приватный туннель, принадлежащий только вам.",
    fa: "VPNهای سنتی بسیاری از کاربران را پشت یک نقطه اتصال مشترک قرار می‌دهند که باعث شلوغی و ناپایداری می‌شود. NullVPN رویکرد کاملاً متفاوتی دارد: یک تونل شخصی که فقط متعلق به خودتان است.",
    ar: "تضع شبكات VPN التقليدية عددًا كبيرًا من المستخدمين خلف نقطة اتصال مشتركة واحدة، فتصبح مزدحمة وغير متسقة. يتبع NullVPN نهجًا مختلفًا جذريًا: نفق خاص يخصك وحدك.",
    es: "Las VPN tradicionales meten a muchos usuarios detrás de un mismo punto de conexión compartido, lo que las hace saturadas e inconsistentes. NullVPN adopta un enfoque fundamentalmente distinto: un túnel privado que es solo tuyo.",
    ne: "परम्परागत VPN ले धेरै प्रयोगकर्ताहरूलाई एउटै साझेदार जडान बिन्दुमा राख्छ, जसले गर्दा ती भीड र असंगत हुन्छन्। NullVPN ले एउटै मूलभूत अलग दृष्टिकोण लिन्छ: तपाईंको एउटै व्यक्तिगत टनेल।",
    fr: "Les VPN traditionnels placent de nombreux utilisateurs derrière un même point de connexion partagé, ce qui les rend saturés et irréguliers. NullVPN adopte une approche fondamentalement différente : un tunnel privé qui n'appartient qu'à vous.",
  },
  "feat.table.feature": {
    en: "Feature",
    ru: "Возможность",
    fa: "ویژگی",
    ar: "الميزة",
    es: "Característica",
    ne: "विशेषता",
    fr: "Caractéristique",
  },
  "feat.table.detail": {
    en: "Details",
    ru: "Подробнее",
    fa: "جزئیات",
    ar: "التفاصيل",
    es: "Detalles",
    ne: "विवरण",
    fr: "Détails",
  },
  "feat.note.h": {
    en: "Designed around one goal",
    ru: "Спроектировано вокруг одной цели",
    fa: "طراحی شده حول یک هدف",
    ar: "مصمّم حول هدف واحد",
    es: "Diseñado en torno a un objetivo",
    ne: "एउटै लक्ष्यमा डिजाइन गरिएको",
    fr: "Conçu autour d'un seul objectif",
  },
  "feat.note.p1": {
    en: "Every feature serves one purpose: a connection that reliably works wherever you are — mobile data, fixed broadband, or demanding networks. Privacy and reliability are not add-ons here; they are the product.",
    ru: "Каждая функция служит одной цели: соединению, которое надёжно работает где угодно — мобильная сеть, проводной интернет или сложные сети. Приватность и надёжность — не дополнения, а сам продукт.",
    fa: "هر ویژگی یک هدف را دنبال می‌کند: اتصالی که هر جا باشید به‌طور قابل اعتماد کار می‌کند — داده موبایل، اینترنت ثابت یا شبکه‌های دشوار. حریم خصوصی و قابلیت اطمینان اینجا افزونه نیستند؛ خودِ محصول‌اند.",
    ar: "كل ميزة تخدم هدفًا واحدًا: اتصال يعمل بموثوقية أينما كنت — بيانات الجوال، أو الخط الثابت، أو الشبكات المتطلبة. الخصوصية والموثوقية هنا ليست إضافات؛ بل هي المنتج نفسه.",
    es: "Cada característica sirve a un solo propósito: una conexión que funciona de forma fiable dondequiera que estés — datos móviles, banda ancha fija o redes exigentes. Aquí la privacidad y la fiabilidad no son extras; son el producto.",
    ne: "हरेक विशेषताले एउटै उद्देश्य सेवा गर्छ: एउटै जडान जुन तपाईं कहाँ छौं भन्ने बारे निर्भर गर्दै चल्छ — मोबाइल डाटा, निश्चित ब्रोडब्यान्ड, वा आवश्यक नेटवर्कहरू। गोपनीयता र विश्वसनीयता यहाँ थप विशेषता होइन; ती उत्पादन नै हुन्।",
    fr: "Chaque caractéristique sert un seul but : une connexion qui fonctionne de manière fiable où que vous soyez — données mobiles, broadband fixe ou réseaux exigeants. Ici, la confidentialité et la fiabilité ne sont pas des options : elles sont le produit.",
  },
  "feat.note.p2": {
    en: "If one access channel is unavailable, another one works. If the website is unreachable, Telegram and the Web3 mirror still deliver your configuration.",
    ru: "Если один канал недоступен, работает другой. Даже без доступа к сайту конфигурация приходит через Telegram и Web3-зеркало.",
    fa: "اگر یک کانال دسترسی در دسترس نباشد، کانال دیگری کار می‌کند. اگر وبسایت غیرقابل دسترس باشد، Telegram و آینه Web3 همچنان پیکربندی شما را تحویل می‌دهند.",
    ar: "إذا تعذّر قناة وصول، تعمل قناة أخرى. وإذا تعذّر الوصول إلى الموقع، يواصل Telegram ومرآة Web3 توصيل إعداداتك.",
    es: "Si un canal de acceso no está disponible, otro funciona. Si el sitio web es inaccesible, Telegram y el espejo Web3 siguen entregando tu configuración.",
    ne: "यदि एउटै पहुँच च्यानल अनुपलब्ध छ, अर्को एउटै काम गर्छ। यदि वेबसाइट पहुँच योग्य छैन, टेलिग्राम र Web3 मिरर अझै तपाईंको कन्फिगरेसन दिन्छन्।",
    fr: "Si un canal d'accès est indisponible, un autre fonctionne. Si le site est inaccessible, Telegram et le miroir Web3 continuent de vous transmettre votre configuration.",
  },
  "price.h": {
    en: "Pricing",
    ru: "Тарифы",
    fa: "قیمت‌ها",
    ar: "الأسعار",
    es: "Precios",
    ne: "मूल्य निर्धारण",
    fr: "Tarifs",
  },
  "checkout.title": {
    en: "Checkout",
    ru: "Оформление",
    fa: "پرداخت",
    ar: "إتمام الدفع",
    es: "Pago",
    ne: "भुक्तानी",
    fr: "Paiement",
  },
  "checkout.handoff.lead": {
    en: "Our Telegram bot is a backup purchase channel — pay there with debit/credit cards or crypto (TON / USDT).",
    ru: "Telegram-бот — резервный канал покупки: там можно оплатить картой или криптовалютой (TON / USDT).",
    fa: "ربات تلگرام کانال خرید جایگزین ماست — آنجا با کارت بانکی یا رمزارز (TON / USDT) پرداخت کنید.",
    ar: "بوت تيليجرام هو قناة الشراء الاحتياطية — ادفع هناك ببطاقة بنكية أو عملات رقمية (TON / USDT).",
    es: "Nuestro bot de Telegram es un canal de compra alternativo — paga allí con tarjeta de débito/crédito o cripto (TON / USDT).",
    ne: "हाम्रो टेलिग्राम बट बैकअप खरिद माध्यम हो — त्यहाँ डेबिट/क्रेडिट कार्ड वा क्रिप्टो (TON / USDT) बाट भुक्तानी गर्नुहोस्।",
    fr: "Notre bot Telegram est un canal d’achat de secours — payez-y par carte bancaire ou en crypto (TON / USDT).",
  },
  "checkout.handoff.cta": {
    en: "Continue in Telegram Bot →",
    ru: "Продолжить в Telegram-боте →",
    fa: "ادامه در ربات تلگرام →",
    ar: "المتابعة في بوت تيليجرام →",
    es: "Continuar en el bot de Telegram →",
    ne: "टेलिग्राम बोटमा जारी राख्नुहोस् →",
    fr: "Continuer dans le bot Telegram →",
  },
  "checkout.handoff.note": {
    en: "Your subscription activates automatically after payment.",
    ru: "Подписка активируется автоматически после оплаты.",
    fa: "اشتراک شما پس از پرداخت به‌طور خودکار فعال می‌شود.",
    ar: "يتم تنشيط اشتراكك تلقائيًا بعد الدفع.",
    es: "Tu suscripción se activa automáticamente después del pago.",
    ne: "भुक्तानीपछि तपाईंको सदस्यता स्वतः सक्रिय हुन्छ।",
    fr: "Votre abonnement s'active automatiquement après le paiement.",
  },
  "checkout.online.lead": {
    en: "Pay by debit/credit cards or crypto (TON / USDT) on our secure checkout.",
    ru: "Оплата картой, СБП или криптовалютой (TON / USDT) на защищённой странице оплаты.",
    fa: "پرداخت با کارت، شتاب یا رمزارز (TON / USDT) در صفحه پرداخت امن ما.",
    ar: "ادفع بالبطاقة المصرفية أو العملات الرقمية (TON / USDT) على صفحة الدفع الآمنة.",
    es: "Paga con tarjeta de débito/crédito o cripto (TON / USDT) en nuestro pago seguro.",
    ne: "हाम्रो सुरक्षित भुक्तानी पृष्ठमा डेबिट/क्रेडिट कार्ड वा क्रिप्टो (TON / USDT) बाट भुक्तानी गर्नुहोस्।",
    fr: "Payez par carte bancaire ou crypto (TON / USDT) sur notre paiement sécurisé.",
  },
  "checkout.online.cta": {
    en: "Pay online — secure checkout →",
    ru: "Оплатить онлайн — защищённая оплата →",
    fa: "پرداخت آنلاین — درگاه امن →",
    ar: "الدفع عبر الإنترنت — دفع آمن →",
    es: "Pagar online — pago seguro →",
    ne: "अनलाइन भुक्तानी — सुरक्षित भुक्तानी →",
    fr: "Payer en ligne — paiement sécurisé →",
  },
  "price.p1.name": {
    en: "Monthly",
    ru: "На месяц",
    fa: "ماهانه",
    ar: "شهري",
    es: "Mensual",
    ne: "महिनाको",
    fr: "Mensuel",
  },
  "price.p3.name": {
    en: "Quarterly",
    ru: "На квартал",
    fa: "فصلی",
    ar: "ربع سنوي",
    es: "Trimestral",
    ne: "त्रैमासिक",
    fr: "Trimestriel",
  },
  "price.p4.name": {
    en: "Annual",
    ru: "На год",
    fa: "سالانه",
    ar: "سنوي",
    es: "Anual",
    ne: "वार्षिक",
    fr: "Annuel",
  },
  "price.permon": {
    en: "/mo",
    ru: "/мес",
    fa: "/ماه",
    ar: "/شهر",
    es: "/mes",
    ne: "/महिना",
    fr: "/mois",
  },
  "price.perqtr": {
    en: "/3 mo",
    ru: "/3 мес",
    fa: "/3 ماه",
    ar: "/3 أشهر",
    es: "/3 meses",
    ne: "/३ महिना",
    fr: "/3 mois",
  },
  "price.peryear": {
    en: "/yr",
    ru: "/год",
    fa: "/سال",
    ar: "/سنة",
    es: "/año",
    ne: "/वर्ष",
    fr: "/an",
  },
  "price.feat.1": {
    en: "✔ Up to 10 devices",
    ru: "✔ До 10 устройств",
    fa: "✔ تا ۱۰ دستگاه",
    ar: "✔ حتى ١٠ أجهزة",
    es: "✔ Hasta 10 dispositivos",
    ne: "✔ १० सम्म उपकरणहरू",
    fr: "✔ Jusqu'à 10 appareils",
  },
  "price.feat.2": {
    en: "✔ Unlimited bandwidth",
    ru: "✔ Безлимитный трафик",
    fa: "✔ پهنای باند نامحدود",
    ar: "✔ نطاق تردد غير محدود",
    es: "✔ Ancho de banda ilimitado",
    ne: "✔ असीमित ब्यान्डविथ",
    fr: "✔ Bande passante illimitée",
  },
  "price.feat.3": {
    en: "✔ Private tunnel endpoint",
    ru: "✔ Выделенная точка туннеля",
    fa: "✔ نقطه اتصال تونل شخصی",
    ar: "✔ نقطة اتصال لنفق خاص",
    es: "✔ Punto de conexión de túnel privado",
    ne: "✔ व्यक्तिगत टनेल जडान बिन्दु",
    fr: "✔ Point de connexion de tunnel privé",
  },
  "price.feat.4": {
    en: "✔ Works on demanding networks",
    ru: "✔ Работает в сложных сетях",
    fa: "✔ کار در شبکه‌های دشوار",
    ar: "✔ يعمل على الشبكات المتطلبة",
    es: "✔ Funciona en redes exigentes",
    ne: "✔ आवश्यक नेटवर्कहरूमा काम गर्छ",
    fr: "✔ Fonctionne sur les réseaux exigeants",
  },
  "price.feat.5": {
    en: "✔ Auto-provisioned instantly",
    ru: "✔ Мгновенное автоподключение",
    fa: "✔ تأمین خودکار فوری",
    ar: "✔ تجهيز تلقائي فوري",
    es: "✔ Aprovisionamiento automático al instante",
    ne: "✔ तुरुन्तै स्वचालित रूपमा उपलब्ध",
    fr: "✔ Provisionné automatiquement, instantanément",
  },
  "price.feat.6": {
    en: "✔ No activity logs",
    ru: "✔ Без журналов активности",
    fa: "✔ بدون گزارش فعالیت",
    ar: "✔ بلا سجلات نشاط",
    es: "✔ Sin registros de actividad",
    ne: "✔ कुनै गतिविधि लगहरू छैनन्",
    fr: "✔ Aucun journal d'activité",
  },
  "price.feat.7": {
    en: "✔ Priority Telegram support",
    ru: "✔ Приоритетная поддержка в Telegram",
    fa: "✔ پشتیبانی اولویتی تلگرام",
    ar: "✔ دعم Telegram بأولوية",
    es: "✔ Soporte prioritario por Telegram",
    ne: "✔ प्राथमिक टेलिग्राम समर्थन",
    fr: "✔ Assistance Telegram prioritaire",
  },
  "price.cta.h": {
    en: "Ready when you are.",
    ru: "Готовы, когда вы.",
    fa: "وقتی شما آماده باشید.",
    ar: "جاهز متى ما كنت جاهزًا.",
    es: "Listo cuando tú lo estés.",
    ne: "तपाईं तयार भएपछि।",
    fr: "Prêt quand vous l'êtes.",
  },
  "price.cta.btn": {
    en: "View Plans →",
    ru: "Смотреть тарифы →",
    fa: "مشاهده طرح‌ها →",
    ar: "استعرض الخطط →",
    es: "Ver planes →",
    ne: "योजनाहरू हेर्नुहोस् →",
    fr: "Voir les forfaits →",
  },
  "price.howpay.h": {
    en: "How payment works",
    ru: "Как проходит оплата",
    fa: "نحوه پرداخت",
    ar: "كيف يعمل الدفع",
    es: "Cómo funciona el pago",
    ne: "भुक्तानी कसरी हुन्छ",
    fr: "Comment fonctionne le paiement",
  },
  "web3.h1": {
    en: "Opening NullVPN on TON…",
    ru: "Открываем NullVPN на TON…",
    fa: "باز کردن NullVPN روی TON...",
    ar: "جارٍ فتح NullVPN على TON…",
    es: "Abriendo NullVPN en TON…",
    ne: "TON मा NullVPN खोल्दै…",
    fr: "Ouverture de NullVPN sur TON…",
  },
  "web3.sub": {
    en: "You're being redirected to NullVPN's decentralised Web3 site on the TON Network — a mirror of this page that works in any browser.",
    ru: "Вы перенаправляетесь на децентрализованное Web3-зеркало NullVPN в сети TON — страницу, которая работает в любом браузере.",
    fa: "شما در حال هدایت به سایت غیرمتمرکز Web3 NullVPN در شبکه TON هستید - آینه این صفحه که در هر مرورگری کار می‌کند.",
    ar: "يتم إعادة توجيهك إلى موقع NullVPN اللامركزي على شبكة TON — نسخة مرآة من هذه الصفحة تعمل في أي متصفح.",
    es: "Te estamos redirigiendo al sitio Web3 descentralizado de NullVPN en la red TON — un espejo de esta página que funciona en cualquier navegador.",
    ne: "तपाईंलाई TON नेटवर्कमा रहेको NullVPN को विकेन्द्रीकृत Web3 साइटमा — यस पृष्ठको एउटा दर्पण जुन कुनै पनि ब्राउजरमा काम गर्दछ, रिडाइरेक्ट गरिँदैछ।",
    fr: "Vous êtes en train d'être redirigé vers le site Web3 décentralisé de NullVPN sur le réseau TON — un miroir de cette page qui fonctionne dans n'importe quel navigateur.",
  },
  "web3.redirecting": {
    en: "Connecting to TON…",
    ru: "Подключение к TON…",
    fa: "اتصال به TON...",
    ar: "جارٍ الاتصال بـ TON…",
    es: "Conectando a TON…",
    ne: "TON मा जडान हुँदैछ...",
    fr: "Connexion à TON…",
  },
  "web3.manual": {
    en: "Not redirected? Open the mirror manually:",
    ru: "Не перенаправило? Откройте зеркало вручную:",
    fa: "به طور خودکار هدایت نشدید؟ آینه را به صورت دستی باز کنید:",
    ar: "لم يتم التحويل؟ افتح المرآة يدويًا:",
    es: "¿No se redirigió? Abre el espejo manualmente:",
    ne: "रिडाइरेक्ट भएन? दर्पणलाई म्यानुअल रूपमा खोल्नुहोस्:",
    fr: "Pas de redirection ? Ouvrez le miroir manuellement :",
  },
  "comp.row.works.strict": {
    en: "Works on restrictive networks",
    ru: "Работает в ограниченных сетях",
    fa: "کار در شبکه‌های محدودشده",
    ar: "يعمل على الشبكات المقيدة",
    es: "Funciona en redes restrictivas",
    ne: "प्रतिबन्धात्मक नेटवर्कहरूमा काम गर्दछ",
    fr: "Fonctionne sur les réseaux restrictifs",
  },
  "comp.row.works.mobile": {
    en: "Works behind strict NAT and firewalls at work/school",
    ru: "Работает за строгим NAT и межсетевыми экранами в офисе/школе",
    fa: "کار در پشت NAT و فایروال‌های سخت در محل کار/مدرسه",
    ar: "يعمل خلف NAT صارم وجدران الحماية في العمل/المدرسة",
    es: "Funciona tras NAT estricta y cortafuegos en el trabajo/escuela",
    ne: "कार्यस्थल/विद्यालयमा कडा NAT र फायरवाल पछि काम गर्दछ",
    fr: "Fonctionne derrière un NAT strict et des pare-feu au travail/à l'école",
  },
  "faq.q10": {
    en: "What is TON?",
    ru: "Что такое TON?",
    fa: "TON چیست؟",
    ar: "ما هو TON؟",
    es: "¿Qué es TON?",
    ne: "TON भनेको के हो?",
    fr: "Qu'est-ce que TON ?",
  },
  "faq.a10": {
    en: "TON is a fast, low-fee blockchain. Toncoin (TON) and USDT-TON are widely available on major exchanges — one of several accepted payment methods alongside debit/credit cards.",
    ru: "TON — быстрый блокчейн с низкими комиссиями. Toncoin (TON) и USDT-TON доступны на крупных биржах — один из способов оплаты наряду с картой и СБП.",
    fa: "TON یک بلاکچین سریع و با کارمزد کم است. Toncoin (TON) و USDT-TON در صرافی‌های اصلی به طور گسترده در دسترس هستند - یکی از روش‌های پرداخت پذیرفته شده به همراه کارت‌های اعتباری/دبیت.",
    ar: "TON هي بلوكشين سريعة ومنخفضة الرسوم. عملة Toncoin (TON) وUSDT-TON متاحان على نطاق واسع في أكبر منصات التداول — إحدى عدة طرق دفع مقبولة إلى جانب البطاقات البنكية.",
    es: "TON es una blockchain rápida y con comisiones bajas. Toncoin (TON) y USDT-TON están disponibles en los principales exchanges — uno de varios métodos de pago aceptados junto con las tarjetas de débito/crédito.",
    ne: "TON एक छिटो, कम शुल्क भएको ब्लकचेन हो। टनकोइन (TON) र USDT-TON मुख्य एक्सचेञ्जहरूमा व्यापक रूपमा उपलब्ध छन् — डेबिट/क्रेडिट कार्डसँगै स्वीकृत भुक्तानी विधिहरू मध्ये एक।",
    fr: "TON est une blockchain rapide et à frais réduits. Toncoin (TON) et USDT-TON sont largement disponibles sur les principales plateformes d'échange — l'un des plusieurs moyens de paiement acceptés en plus des cartes bancaires.",
  },
  "faq.q_adguard": {
    en: "What is Ad Guard?",
    ru: "Что такое Ad Guard?",
    fa: "Ad Guard چیست؟",
    ar: "ما هو Ad Guard؟",
    es: "¿Qué es Ad Guard?",
    ne: "Ad Guard भनेको के हो?",
    fr: "Qu'est-ce qu'Ad Guard ?",
  },
  "faq.a_adguard": {
    en: "Ad Guard is a network-level ad and tracker blocker built into your tunnel. Because filtering happens before traffic reaches your device, it covers every app and browser at once — no extensions or per-app setup. It is currently in development and will be enabled for subscribers automatically when it ships.",
    ru: "Ad Guard — сетевой блокировщик рекламы и трекеров внутри вашего туннеля. Фильтрация происходит до того, как трафик достигнет устройства, — охватывает все приложения и браузеры сразу, без расширений. Функция в разработке и будет включена абонентам автоматически.",
    fa: "Ad Guard یک مسدودکننده سطح شبکه برای تبلیغات و ردیاب است که در تونل شما تعبیه شده است. از آنجایی که فیلترسازی قبل از اینکه ترافیک به دستگاه شما برسد انجام می‌شود، همه برنامه‌ها و مرورگرها را یکجا پوشش می‌دهد - بدون نیاز به افزونه یا تنظیمات برنامه‌ای. در حال حاضر در حال توسعه است و برای مشترکین به صورت خودکار فعال خواهد شد.",
    ar: "Ad Guard هو حاجب إعلانات ومتتبعات على مستوى الشبكة مدمج في نفقك. ولأن التصفية تحدث قبل وصول البيانات إلى جهازك، يغطي كل التطبيقات والمتصفحات دفعة واحدة — دون إضافات أو إعداد لكل تطبيق. هو حاليًا قيد التطوير وسيُفعَّل تلقائيًا للمشتركين عند إطلاقه.",
    es: "Ad Guard es un bloqueador de anuncios y rastreadores a nivel de red integrado en tu túnel. Como el filtrado ocurre antes de que el tráfico llegue a tu dispositivo, cubre todas las apps y navegadores a la vez — sin extensiones ni configuraciones por aplicación. Actualmente está en desarrollo y se activará automáticamente para los suscriptores cuando esté listo.",
    ne: "Ad Guard तपाईंको टनेलमा निर्मित एक नेटवर्क-स्तरीय विज्ञापन र ट्र्याकर ब्लकर हो। चाहिएको फिल्टरिङ ट्राफिक तपाईंको डिभाइससम्म पुग्नु अघि हुने भएकोले, यसले एकै पटक सबै एप र ब्राउजरलाई ढाक्छ — कुनै एक्सटेन्सन वा प्रति-एप सेटअप चाहिँदैन। यो वर्तमानमा विकासमा छ र जब यसलाई सार्वजनिक गरिन्छ, त्यसपछि यसलाई सदस्यहरूका लागि स्वचालित रूपमा सक्षम बनाइनेछ।",
    fr: "Ad Guard est un bloqueur de publicités et de traqueurs au niveau du réseau, intégré à votre tunnel. Comme le filtrage se produit avant que le trafic n'atteigne votre appareil, il couvre toutes les applications et tous les navigateurs à la fois — sans extensions ni réglages par application. Actuellement en développement, il sera activé automatiquement pour les abonnés dès sa sortie.",
  },
  "price.p1.note": {
    en: "Debit/credit cards or crypto",
    ru: "Карта, СБП или крипта",
    fa: "کارت‌های دبیت/اعتباری یا کریپتو",
    ar: "بطاقة بنكية أو عملة رقمية",
    es: "Tarjeta de débito/crédito o cripto",
    ne: "डेबिट/क्रेडिट कार्ड वा क्रिप्टो",
    fr: "Carte bancaire ou crypto",
  },
  "price.p3.note": {
    en: "Billed every 3 months — $10",
    ru: "Оплата раз в 3 месяца — 1 000 ₽",
    fa: "پرداخت هر ۳ ماه یک‌بار — ۱۰ دلار",
    ar: "تُحسب كل 3 أشهر — $10",
    es: "Cobro cada 3 meses — $10",
    ne: "3 महिनामा एप गरिन्छ — $10",
    fr: "Facturé tous les 3 mois — $10",
  },
  "price.p4.note": {
    en: "Billed once a year — $35",
    ru: "Оплата раз в год — 3 500 ₽",
    fa: "پرداخت سالانه یک‌بار — ۳۵ دلار",
    ar: "تُحسب مرة في السنة — $35",
    es: "Cobro una vez al año — $35",
    ne: "एक वर्षमा एप गरिन्छ — $35",
    fr: "Facturé une fois par an — $35",
  },
  "price.cta.p": {
    en: "Pay with debit/credit cards or crypto — connect right away. That’s it.",
    ru: "Оплата картой, СБП или криптой — и сразу на связи. Вот и всё.",
    fa: "با کارت بانکی یا رمزارز پرداخت کنید — بلافاصله متصل شوید. همین.",
    ar: "ادفع ببطاقة بنكية أو عملة رقمية — واتصل على الفور. هذا كل شيء.",
    es: "Paga con tarjeta de débito/crédito o cripto — conéctate al instante. Así de simple.",
    ne: "डेबिट/क्रेडिट कार्ड वा क्रिप्टोबाट तिर्नुहोस् — तत्कालै जडान गर्नुहोस्। यो मात्रै।",
    fr: "Payez par carte bancaire ou en crypto — connectez-vous aussitôt. C'est tout.",
  },
  "price.howpay.p1": {
    en: "Prices are shown in USD (₽300/mo for card & SBP payments in Russia). Pay with debit/credit cards or crypto (USDT / TON) — your connection is provisioned automatically within seconds.",
    ru: "Цены указаны в рублях для оплаты картой или СБП; криптовалютой (USDT / TON) — по текущему курсу. Подключение — автоматически за секунды.",
    fa: "قیمت‌ها به دلار آمریکا است (برای پرداخت کارت/شتاب در روسیه: ۳۰۰ روبل در ماه). پرداخت با کارت بانکی یا رمزارز (USDT / TON) — اتصال شما ظرف چند ثانیه به‌صورت خودکار آماده می‌شود.",
    ar: "الأسعار معروضة بالدولار الأمريكي (₽300 شهريًا للدفع بالبطاقة وSBP في روسيا). ادفع ببطاقة بنكية أو عملة رقمية (USDT / TON) — يُجهَّز اتصالك تلقائيًا خلال ثوانٍ.",
    es: "Los precios se muestran en USD (₽300/mes para pagos con tarjeta y SBP en Rusia). Paga con tarjeta de débito/crédito o cripto (USDT / TON) — tu conexión se aprovisiona automáticamente en segundos.",
    ne: "मूल्यहरू USD मा देखाइएको छ (रूसमा कार्ड र SBP भुक्तानीका लागि $300/महिना)। डेबिट/क्रेडिट कार्ड वा क्रिप्टो (USDT / TON) मा भुक्तान गर्नुहोस् — तपाईंको जडान सेकेन्डभित्र स्वचालित रूपमा व्यवस्थित गरिन्छ।",
    fr: "Les prix sont affichés en USD (₽300/mois pour les paiements par carte et SBP en Russie). Payez par carte bancaire ou en crypto (USDT / TON) — votre connexion est provisionnée automatiquement en quelques secondes.",
  },
  "price.howpay.p2": {
    en: "Sign in with an access token — no passwords, no forms to fill in.",
    ru: "Вход по токену доступа — без паролей и форм.",
    fa: "ورود با توکن دسترسی — بدون رمز عبور و بدون فرم.",
    ar: "سجّل الدخول برمز وصول — بلا كلمات مرور وبلا نماذج.",
    es: "Inicia sesión con un token de acceso — sin contraseñas ni formularios.",
    ne: "एक्सेस टोकनसँग साइन इन गर्नुहोस् — कुनै पासवर्ड, कुनै फारम भर्नुपर्दैन।",
    fr: "Connectez-vous avec un jeton d'accès — sans mot de passe, sans formulaire.",
  },
  "index.f5.h": {
    en: "Ad Guard coming soon",
    ru: "Ad Guard — скоро",
    fa: "Ad Guard به‌زودی",
    ar: "Ad Guard قريبًا",
    es: "Ad Guard próximamente",
    ne: "Ad Guard चाँडै आउँदैछ",
    fr: "Ad Guard bientôt disponible",
  },
  "index.f5.p": {
    en: "Network-level ad and tracker filtering built right into your tunnel — covering every app and device behind it, no extensions needed. In development now; subscribers get it automatically when it ships.",
    ru: "Блокировка рекламы и трекеров на сетевом уровне прямо в вашем туннеле — охватывает все приложения и устройства без расширений. Сейчас в разработке; абоненты получат её автоматически при выпуске.",
    fa: "فیلترینگ تبلیغات و ردیاب‌ها در سطح شبکه، مستقیم در تونل شما — همه اپ‌ها و دستگاه‌های پشت آن را پوشش می‌دهد، بدون نیاز به افزونه. در حال توسعه است؛ مشترکین هنگام انتشار به‌طور خودکار دریافت می‌کنند.",
    ar: "تصفية الإعلانات والمتتبعات على مستوى الشبكة مدمجة في نفقك — تغطي كل التطبيقات والأجهزة خلفه، دون الحاجة إلى إضافات. قيد التطوير الآن؛ سيحصل المشتركون عليها تلقائيًا عند إطلاقها.",
    es: "Filtrado de anuncios y rastreadores a nivel de red integrado en tu túnel — cubre todas las aplicaciones y dispositivos detrás de él, sin extensiones. En desarrollo ahora; los suscriptores lo recibirán automáticamente cuando esté disponible.",
    ne: "तपाईंको टनलभित्रै नेटवर्क-स्तरको विज्ञापन र ट्र्याकर फिल्टरिङ — पछाडिका सबै एप र उपकरणहरूलाई समेट्छ, एक्सटेन्सन आवश्यक छैन। अहिले विकासाधीन; ग्राहकहरूले जारी हुनासाथ स्वतः प्राप्त गर्नेछन्।",
    fr: "Filtrage des publicités et trackers au niveau du réseau intégré à votre tunnel — couvre toutes les applications et tous les appareils derrière lui, sans extension. En développement ; les abonnés le recevront automatiquement dès sa sortie.",
  },
  "nav.home": {
    en: "Home",
    ru: "Главная",
    fa: "خانه",
    ar: "الرئيسية",
    es: "Inicio",
    ne: "गृह",
    fr: "Accueil",
  },
  "nav.features": {
    en: "Features",
    ru: "Возможности",
    fa: "ویژگی‌ها",
    ar: "الميزات",
    es: "Funciones",
    ne: "विशेषताहरू",
    fr: "Fonctionnalités",
  },
  "nav.how": {
    en: "How It Works",
    ru: "Как работает",
    fa: "نحوه کار",
    ar: "كيف يعمل",
    es: "Cómo funciona",
    ne: "कसरी काम गर्छ",
    fr: "Comment ça marche",
  },
  "nav.pricing": {
    en: "Pricing",
    ru: "Цены",
    fa: "قیمت‌ها",
    ar: "الأسعار",
    es: "Precios",
    ne: "मूल्य",
    fr: "Tarifs",
  },
  "nav.faq": {
    en: "FAQ",
    ru: "FAQ",
    fa: "سوالات متداول",
    ar: "الأسئلة الشائعة",
    es: "FAQ",
    ne: "सामान्य प्रश्नहरू",
    fr: "FAQ",
  },
  "nav.contact": {
    en: "Contact",
    ru: "Контакты",
    fa: "تماس",
    ar: "اتصل بنا",
    es: "Contacto",
    ne: "सम्पर्क",
    fr: "Contact",
  },
  "nav.compare": {
    en: "Compare",
    ru: "Сравнение",
    fa: "مقایسه",
    ar: "قارن",
    es: "Comparar",
    ne: "तुलना",
    fr: "Comparatif",
  },
  "nav.download": {
    en: "Download App",
    ru: "Скачать приложение",
    fa: "دانلود برنامه",
    ar: "حمّل التطبيق",
    es: "Descargar app",
    ne: "एप डाउनलोड गर्नुहोस्",
    fr: "Télécharger l’app",
  },
  "nav.cta.buy": {
    en: "Buy Premium",
    ru: "Купить подписку",
    fa: "خرید اشتراک",
    ar: "اشترِ Premium",
    es: "Comprar Premium",
    ne: "प्रीमियम किन्नुहोस्",
    fr: "Acheter Premium",
  },
  "index.f1.h": {
    en: "Not a regular VPN",
    ru: "Не обычный VPN",
    fa: "VPN معمولی نیست",
    ar: "ليس VPN تقليديًا",
    es: "No es una VPN común",
    ne: "नियमित VPN होइन",
    fr: "Pas un VPN ordinaire",
  },
  "index.f1.p": {
    en: "Your traffic travels through a private, fully encrypted tunnel that belongs to you alone. Strong end-to-end encryption keeps your activity yours — on any network.",
    ru: "Трафик идёт по приватному полностью зашифрованному туннелю, принадлежащему только вам. Сквозное шифрование сохраняет вашу активность вашей — в любой сети.",
    fa: "ترافیک شما از یک تونل خصوصی و کاملاً رمزنگاری‌شده عبور می‌کند که فقط متعلق به شماست. رمزنگاری قوی سرتاسری فعالیت شما را — در هر شبکه‌ای — خصوصی نگه می‌دارد.",
    ar: "ينقل مرورك عبر نفق خاص مشفّر بالكامل يخصك وحدك. التشفير القوي من الطرف إلى الطرف يحافظ على خصوصية نشاطك — على أي شبكة.",
    es: "Tu tráfico viaja por un túnel privado y completamente cifrado que te pertenece solo a ti. El cifrado sólido de extremo a extremo mantiene tu actividad como tuya — en cualquier red.",
    ne: "तपाईंको ट्राफिक निजी, पूर्ण इन्क्रिप्टेड टनलबाट जान्छ जुन तपाईं एक्लैको हो। बलियो एन्ड-टु-एन्ड इन्क्रिप्शनले तपाईंको गतिविधि — कुनै पनि नेटवर्कमा — तपाईंकै राख्छ।",
    fr: "Votre trafic circule dans un tunnel privé entièrement chiffré qui n'appartient qu'à vous. Le chiffrement fort de bout en bout garde votre activité privée — sur n'importe quel réseau.",
  },
  "index.f2.h": {
    en: "Resilient routes.",
    ru: "Устойчивые маршруты.",
    fa: "مسیرهای تاب‌آور.",
    ar: "مسارات مرنة.",
    es: "Rutas resilientes.",
    ne: "लचिला मार्गहरू।",
    fr: "Routes résilientes.",
  },
  "index.f2.p": {
    en: "If one connection path becomes unavailable, your tunnel can switch to another available route. Performance and availability depend on your device, provider, and network conditions.",
    ru: "Если одно направление соединения недоступно, туннель может переключиться на другой доступный маршрут. Скорость и доступность зависят от вашего устройства, провайдера и условий сети.",
    fa: "اگر یک مسیر اتصال در دسترس نباشد، تونل شما می‌تواند به مسیر دیگری سوئیچ کند. سرعت و دسترسی به دستگاه، ارائه‌دهنده و شرایط شبکه شما بستگی دارد.",
    ar: "إذا أصبح أحد مسارات الاتصال غير متاح، يمكن لنفقك التبديل إلى مسار آخر متاح. يعتمد الأداء والتوفر على جهازك ومزودك وظروف شبكتك.",
    es: "Si una ruta de conexión deja de estar disponible, tu túnel puede cambiar a otra disponible. El rendimiento y la disponibilidad dependen de tu dispositivo, tu proveedor y las condiciones de la red.",
    ne: "कुनै जडान मार्ग अनुपलब्ध भएमा, तपाईंको टनल अर्को उपलब्ध मार्गमा स्विच गर्न सक्छ। प्रदर्शन र उपलब्धता तपाईंको यन्त्र, प्रदायक र नेटवर्क अवस्थामा निर्भर हुन्छ।",
    fr: "Si une route de connexion devient indisponible, votre tunnel peut en emprunter une autre. Les performances et la disponibilité dépendent de votre appareil, de votre opérateur et des conditions du réseau.",
  },
  "index.f3.h": {
    en: "Flexible payments",
    ru: "Гибкая оплата",
    fa: "پرداخت منعطف",
    ar: "دفع مرن",
    es: "Pagos flexibles",
    ne: "लचिलो भुक्तानी",
    fr: "Paiements flexibles",
  },
  "index.f3.p": {
    en: "Pay with debit/credit cards or crypto — processed securely by trusted third-party providers. We never see or store your payment details.",
    ru: "Оплачивайте картой, СБП или криптой — безопасно через проверенных сторонних провайдеров. Мы не видим и не храним ваши платёжные данные.",
    fa: "پرداخت با کارت بانکی یا رمزارز — با پردازش امن توسط ارائه‌دهندگان معتبر شخص ثالث. ما جزئیات پرداخت شما را نمی‌بینیم و ذخیره نمی‌کنیم.",
    ar: "ادفع ببطاقة مصرفية أو العملات الرقمية — تتم المعالجة بأمان عبر مزودين خارجيين موثوقين. لا نرى تفاصيل الدفع الخاصة بك ولا نخزّنها.",
    es: "Paga con tarjeta de débito/crédito o criptomonedas — procesado de forma segura por proveedores externos de confianza. Nunca vemos ni almacenamos tus datos de pago.",
    ne: "डेबिट/क्रेडिट कार्ड वा क्रिप्टोबाट भुक्तानी गर्नुहोस् — विश्वसनीय तेस्रो-पक्ष प्रदायकहरूमार्फत सुरक्षित रूपमा प्रशोधन हुन्छ। हामी तपाईंको भुक्तानी विवरण कहिल्यै देख्दैनौं वा भण्डारण गर्दैनौं।",
    fr: "Payez par carte bancaire ou crypto — traité en toute sécurité par des prestataires tiers de confiance. Nous ne voyons jamais vos données de paiement et ne les stockons pas.",
  },
  "index.f4.h": {
    en: "3 taps. Zero config.",
    ru: "3 нажатия. Нулевая настройка.",
    fa: "۳ ضربه. صفر پیکربندی.",
    ar: "3 لمسات. صفر إعداد.",
    es: "3 toques. Cero configuración.",
    ne: "३ ट्याप। शून्य कन्फिग।",
    fr: "3 gestes. Zéro configuration.",
  },
  "index.f4.p": {
    en: "1. Download and install the app. 2. Sign in with your access token — optional email link delivery, no passwords. 3. Tap connect. Your settings provision themselves automatically.",
    ru: "1. Скачайте и установите приложение. 2. Войдите по токену доступа — доставка на email по желанию, без паролей. 3. Нажмите «Подключить». Настройки применятся автоматически.",
    fa: "۱. برنامه را دانلود و نصب کنید. ۲. با توکن دسترسی خود وارد شوید — ارسال لینک ایمیلی اختیاری است، بدون رمز عبور. ۳. روی «اتصال» بزنید. تنظیمات به‌طور خودکار اعمال می‌شوند.",
    ar: "1. حمّل التطبيق وثبّته. 2. سجّل الدخول برمز الوصول الخاص بك — إرسال الرابط بالبريد الإلكتروني اختياري، بدون كلمات مرور. 3. انقر «اتصال». تُهيَّأ إعداداتك تلقائيًا.",
    es: "1. Descarga e instala la aplicación. 2. Inicia sesión con tu token de acceso — el envío del enlace por correo es opcional, sin contraseñas. 3. Toca conectar. Tu configuración se aprovisiona automáticamente.",
    ne: "१. एप डाउनलोड र इन्स्टल गर्नुहोस्। २. आफ्नो एक्सेस टोकनले साइन इन गर्नुहोस् — इमेल लिंक डेलिभरी ऐच्छिक, पासवर्ड आवश्यक छैन। ३. कनेक्ट थिच्नुहोस्। सेटिङहरू स्वतः लागू हुन्छन्।",
    fr: "1. Téléchargez et installez l'application. 2. Connectez-vous avec votre jeton d'accès — l'envoi du lien par e-mail est facultatif, sans mot de passe. 3. Appuyez sur « Connecter ». Vos réglages se configurent automatiquement.",
  },
  "index.feat.compare": {
    en: "See NullVPN vs NordVPN, ExpressVPN, ProtonVPN →",
    ru: "NullVPN против NordVPN, ExpressVPN, ProtonVPN →",
    fa: "NullVPN در برابر NordVPN، ExpressVPN، ProtonVPN →",
    ar: "قارن NullVPN مع NordVPN وExpressVPN وProtonVPN →",
    es: "Compara NullVPN con NordVPN, ExpressVPN y ProtonVPN →",
    ne: "NullVPN बनाम NordVPN, ExpressVPN, ProtonVPN →",
    fr: "Comparez NullVPN à NordVPN, ExpressVPN et ProtonVPN →",
  },
  "index.notavpn.h": {
    en: "Not just another shared-server VPN",
    ru: "Не просто ещё один VPN с общими серверами",
    fa: "فقط یک VPN مشترک‌سرور دیگر نیست",
    ar: "ليس مجرد VPN آخر بخوادم مشتركة",
    es: "No es otra VPN más con servidores compartidos",
    ne: "साझा सर्भर भएको अर्को VPN मात्र होइन",
    fr: "Pas un VPN de plus à serveurs partagés",
  },
  "index.notavpn.p": {
    en: "Many consumer VPNs route thousands of strangers through the same shared servers and well-known address ranges — which makes connections crowded, slow, and unreliable when you need them most.",
    ru: "Многие потребительские VPN пропускают тысячи незнакомцев через одни и те же общие серверы — соединения перегружены, медленны и ненадёжны.",
    fa: "بسیاری از VPNهای مصرفی هزاران غریبه را از طریق همان سرورهای اشتراکی و بازه‌های IP شناخته‌شده عبور می‌دهند — نتیجه‌اش اتصالات شلوغ، کند و ناپایدار است، همان‌جا که بیشترین نیاز را دارید.",
    ar: "تمرر العديد من خدمات VPN الاستهلاكية آلاف الغرباء عبر نفس الخوادم المشتركة ونطاقات العناوين المعروفة — ما يجعل الاتصالات مزدحمة وبطيئة وغير موثوقة عندما تحتاجها أكثر.",
    es: "Muchas VPN de consumo enrutan a miles de desconocidos por los mismos servidores compartidos y rangos de direcciones conocidos — lo que hace las conexiones saturadas, lentas y poco fiables cuando más las necesitas.",
    ne: "धेरै उपभोक्ता VPN हरूले हजारौं अपरिचित व्यक्तिहरूलाई त्यही साझा सर्भर र परिचित ठेगाना दायराहरूबाट रुट गर्छन् — जसले जडानहरू भीडभाड, ढिलो र अविश्वसनीय बनाउँछ, जब तपाईंलाई सबैभन्दा बढी आवश्यक हुन्छ।",
    fr: "Beaucoup de VPN grand public font passer des milliers d'inconnus par les mêmes serveurs partagés et plages d'adresses connues — d'où des connexions saturées, lentes et peu fiables quand vous en avez le plus besoin.",
  },
  "index.notavpn.p2": {
    en: "NullVPN gives you a private tunnel with dedicated endpoints and automatic backup paths. Your traffic stays encrypted from your device all the way out, and if one route has trouble, another takes over. <strong>Reliability by architecture, not luck.</strong>",
    ru: "NullVPN даёт вам приватный туннель с выделенными точками выхода и автоматическими резервными маршрутами. Если один маршрут даёт сбой, другой подхватывает. <strong>Надёжность заложена в архитектуре.</strong>",
    fa: "NullVPN به شما یک تونل خصوصی با نقاط پایانی اختصاصی و مسیرهای پشتیبان خودکار می‌دهد. ترافیک شما از دستگاه‌تان تا مقصد رمزنگاری‌شده باقی می‌ماند و اگر یک مسیر مشکل پیدا کند، مسیر دیگری جایگزین می‌شود. <strong>قابلیت اطمینان با معماری، نه شانس.</strong>",
    ar: "يمنحك NullVPN نفقًا خاصًا بنقاط نهاية مخصصة ومسارات احتياطية تلقائية. يبقى ترافيكك مشفرًا من جهازك وحتى الخارج، وإذا واجه مسار مشكلة، يتولى مسار آخر المهمة. <strong>الموثوقية بالتصميم، لا بالحظ.</strong>",
    es: "NullVPN te da un túnel privado con endpoints dedicados y rutas de respaldo automáticas. Tu tráfico permanece cifrado desde tu dispositivo hasta la salida, y si una ruta falla, otra toma el relevo. <strong>Fiabilidad por arquitectura, no por suerte.</strong>",
    ne: "NullVPN ले तपाईंलाई समर्पित एन्डपोइन्ट र स्वतः ब्याकअप मार्गसहितको निजी टनल दिन्छ। तपाईंको ट्राफिक उपकरणबाट बाहिरसम्म इन्क्रिप्टेड रहन्छ, र एउटा मार्गमा समस्या भए अर्कोले काम लिन्छ। <strong>भरपर्दोपन आर्किटेक्चरबाट, भाग्यबाट होइन।</strong>",
    fr: "NullVPN vous offre un tunnel privé avec des points de sortie dédiés et des chemins de secours automatiques. Votre trafic reste chiffré de votre appareil jusqu'à la sortie, et si une route a un souci, une autre prend le relais. <strong>La fiabilité par l'architecture, pas par la chance.</strong>",
  },
  "index.notavpn.btn": {
    en: "Full technical comparison →",
    ru: "Полное техническое сравнение →",
    fa: "مقایسه فنی کامل →",
    ar: "المقارنة التقنية الكاملة →",
    es: "Comparación técnica completa →",
    ne: "पूर्ण प्राविधिक तुलना →",
    fr: "Comparaison technique complète →",
  },
  "index.cta.h": {
    en: "Stop playing VPN whack-a-mole.",
    ru: "Хватит играть в «угадай VPN».",
    fa: "دیگر VPN عوض عوض نزنید.",
    ar: "توقف عن لعبة القنص مع شبكات VPN.",
    es: "Deja de jugar al topo con las VPN.",
    ne: "VPN व्ह्याक-ए-मोल खेल्न बन्द गर्नुहोस्।",
    fr: "Arrêtez de jouer au VPN whack-a-mole.",
  },
  "index.cta.p": {
    en: "Get a connection that actually works. From $3/month. Cancel anytime.",
    ru: "Подключение, которое реально работает. От 300 ₽/мес. Отмена в любое время.",
    fa: "اتصالی که واقعاً کار می‌کند. از ۳ دلار/ماه. هر زمان لغو کنید.",
    ar: "احصل على اتصال يعمل فعلًا. ابتداءً من $3 شهريًا. ألغِ متى شئت.",
    es: "Consigue una conexión que de verdad funciona. Desde $3/mes. Cancela cuando quieras.",
    ne: "वास्तवमा काम गर्ने जडान। $3/महिनाबाट। जुनसुकै समय रद्द गर्नुहोस्।",
    fr: "Obtenez une connexion qui fonctionne vraiment. Dès $3/mois. Résiliable à tout moment.",
  },
  "index.cta.btn": {
    en: "Get NullVPN →",
    ru: "Получить NullVPN →",
    fa: "دریافت NullVPN →",
    ar: "احصل على NullVPN →",
    es: "Obtén NullVPN →",
    ne: "NullVPN पाउनुहोस् →",
    fr: "Obtenir NullVPN →",
  },
  "index.feat.h": {
    en: "Why NullVPN works on difficult networks.",
    ru: "Почему NullVPN работает в сложных сетях.",
    fa: "چرا NullVPN در شبکه‌های دشوار کار می‌کند.",
    ar: "لماذا يعمل NullVPN على الشبكات الصعبة.",
    es: "Por qué NullVPN funciona en redes difíciles.",
    ne: "NullVPN किन कठिन नेटवर्कहरूमा काम गर्छ।",
    fr: "Pourquoi NullVPN fonctionne sur les réseaux difficiles.",
  },
  "index.countries.h": {
    en: "Use it wherever you are.",
    ru: "Используйте там, где вы находитесь.",
    fa: "هر جا که هستید استفاده کنید.",
    ar: "استخدمه أينما كنت.",
    es: "Úsalo donde estés.",
    ne: "जहाँ जहाँ हुनुहुन्छ, त्यहीँ प्रयोग गर्नुहोस्।",
    fr: "Utilisez-le où que vous soyez.",
  },
  "index.countries.tagline": {
    en: "Mobile data, home broadband, office networks, and hotel Wi-Fi.",
    ru: "Мобильный интернет, домашний широкополосный доступ, корпоративные сети и Wi-Fi в отелях.",
    fa: "داده همراه، پهنای باند خانگی، شبکه‌های اداری و Wi-Fi هتل.",
    ar: "بيانات الجوال، والإنترنت المنزلي، وشبكات المكاتب، وواي فاي الفنادق.",
    es: "Datos móviles, banda ancha doméstica, redes de oficina y Wi-Fi de hotel.",
    ne: "मोबाइल डाटा, घरायसी ब्रोडब्यान्ड, कार्यालय नेटवर्क र होटल वाई-फाई।",
    fr: "Données mobiles, box domestique, réseaux d'entreprise et Wi-Fi d'hôtel.",
  },
  "feat.h1a": {
    en: "Everything you need.",
    ru: "Всё, что нужно.",
    fa: "همه چیزی که نیاز دارید.",
    ar: "كل ما تحتاجه.",
    es: "Todo lo que necesitas.",
    ne: "तपाईंलाई चाहिने सबै कुरा।",
    fr: "Tout ce qu'il vous faut.",
  },
  "feat.h1b": {
    en: "Nothing you don't.",
    ru: "Ничего лишнего.",
    fa: "و نه چیزی که نیاز ندارید.",
    ar: "لا شيء زائد.",
    es: "Nada que te sobre.",
    ne: "जो चाहिँदैन त्यो छैन।",
    fr: "Rien de superflu.",
  },
  "feat.sub": {
    en: "Built for one purpose — getting you online privately, wherever you are.",
    ru: "Создан с одной целью — обеспечить вам конфиденциальный доступ в сеть, где бы вы ни находились.",
    fa: "برای یک هدف ساخته شده — اینکه شما را به صورت خصوصی آنلاین کند، هر جایی که باشید.",
    ar: "مبني لهدف واحد — إيصالك إلى الإنترنت بخصوصية، أينما كنت.",
    es: "Creado para un solo propósito — conectarte en privado, estés donde estés.",
    ne: "एउटै उद्देश्यका लागि बनाइएको — तपाईं जहाँ भए पनि निजी रूपमा अनलाइन गराउनु।",
    fr: "Conçu pour un seul but — vous mettre en ligne en privé, où que vous soyez.",
  },
  "feat.tag1": {
    en: "Privacy",
    ru: "Конфиденциальность",
    fa: "حریم خصوصی",
    ar: "الخصوصية",
    es: "Privacidad",
    ne: "गोपनीयता",
    fr: "Confidentialité",
  },
  "feat.r1.h": {
    en: "No activity logs, by design",
    ru: "Никаких журналов активности — по дизайну",
    fa: "بدون ثبت فعالیت، در طراحی",
    ar: "بلا سجلات نشاط، بالتصميم",
    es: "Sin registros de actividad, por diseño",
    ne: "गतिविधि लग छैन, डिजाइन अनुसार",
    fr: "Aucun journal d'activité, par conception",
  },
  "feat.r1.p": {
    en: "We never record which sites you visit, what you transmit, or your real IP address. We keep no connection history in logs — on our side or yours. If you use the browser as your client, we recommend private tabs and similar tools so nothing is stored on your device.",
    ru: "Мы не записываем, какие сайты вы посещаете, что передаёте и ваш реальный IP. Мы не храним историю соединений в логах — ни на своей стороне, ни на вашей. Если вы используете браузер как клиент, рекомендуем приватные вкладки, чтобы на устройстве ничего не сохранялось.",
    fa: "ما هرگز ثبت نمی‌کنیم به چه سایت‌هایی می‌روید، چه ارسال می‌کنید یا IP واقعی شما چیست. تاریخچه اتصال روی دستگاه خودتان می‌ماند و هرگز آن را ترک نمی‌کند. ایمیل تنها اطلاعات شخصی است که ذخیره می‌کنیم — صرفاً برای مدیریت حساب. ورود بدون رمز عبور: با یک لمس از طریق لینک ایمیلی.",
    ar: "لا نسجل أبدًا المواقع التي تزورها ولا ما تنقله ولا عنوان IP الحقيقي. لا نحتفظ بأي سجل لاتصالاتك — لا عندنا ولا عندك. إذا كنت تستخدم المتصفح كعميل، نوصي بالتبويبات الخاصة وما يشبهها حتى لا يُخزَّن شيء على جهازك.",
    es: "Nunca registramos qué sitios visitas, qué transmites ni tu dirección IP real. El historial de conexiones permanece en tu dispositivo y nunca lo abandona. Tu correo es el único dato personal que almacenamos — solo para gestionar tu cuenta. Inicia sesión sin contraseña: un toque mediante un enlace por correo.",
    ne: "तपाईंले कुन साइट हेर्नुहुन्छ, के पठाउनुहुन्छ वा तपाईंको वास्तविक IP हामी कहिल्यै रेकर्ड गर्दैनौं। जडान इतिहास तपाईंको आफ्नै यन्त्रमा रहन्छ र कहिल्यै बाहिरिँदैन। तपाईंको इमेल मात्र व्यक्तिगत विवरण हो जुन हामी भण्डारण गर्छौं — केवल खाता सञ्चालनका लागि। पासवर्डबिना साइन इन: इमेल लिंकबाट एक ट्याप।",
    fr: "We never record which sites you visit, what you transmit, or your real IP address. Connection history stays on your own device and never leaves it. Your email is the only personal detail we store — solely to run your account. Sign in without a password: one tap via an email link.",
  },
  "feat.tag2": {
    en: "Reliability",
    ru: "Надёжность",
    fa: "قابلیت اطمینان",
    ar: "الموثوقية",
    es: "Fiabilidad",
    ne: "विश्वसनीयता",
    fr: "Fiabilité",
  },
  "feat.r2.h": {
    en: "Works on difficult networks",
    ru: "Работает в сложных сетях",
    fa: "در شبکه‌های دشوار کار می‌کند",
    ar: "يعمل على الشبكات الصعبة",
    es: "Funciona en redes difíciles",
    ne: "कठिन नेटवर्कहरूमा काम गर्छ",
    fr: "Fonctionne sur les réseaux difficiles",
  },
  "feat.r2.p": {
    en: "NullVPN continuously measures the quality of every available path between you and our infrastructure and keeps the best working route active — automatically.",
    ru: "NullVPN постоянно измеряет качество всех доступных маршрутов и автоматически держит активным лучший работающий путь.",
    fa: "از مبهم‌سازی پیشرفته‌ای استفاده می‌کند که ترافیک تونل را به‌شکل فعالیت عادی وب پنهان می‌کند، بنابراین در هر شبکه‌ای مانند HTTPS معمولی رفتار می‌کند.",
    ar: "يقيس NullVPN باستمرار جودة كل مسار متاح بينك وبين بنيتنا التحتية ويُبقي أفضل مسار عامل نشطًا — تلقائيًا.",
    es: "Utiliza un ofuscamiento avanzado que disfraza el tráfico del túnel como actividad web ordinaria, comportándose como HTTPS normal en cualquier red.",
    ne: "उन्नत अवरोधन प्रयोग गर्छ जसले टनेल ट्राफिकलाई सामान्य वेब गतिविधिको रूपमा लुकाउँछ, त्यसैले कुनै पनि सञ्जालमा सामान्य HTTPS जस्तै व्यवहार गर्छ।",
    fr: "Utilise une obscurcisation avancée qui déguise le trafic du tunnel en activité web ordinaire : il se comporte comme du HTTPS normal sur tout réseau.",
  },
  "feat.tag3": {
    en: "Payments",
    ru: "Платежи",
    fa: "پرداخت‌ها",
    ar: "المدفوعات",
    es: "Pagos",
    ne: "भुगतानहरू",
    fr: "Paiements",
  },
  "feat.r3.h": {
    en: "Pay your way",
    ru: "Оплачивайте как удобно",
    fa: "به روش خودتان پرداخت کنید",
    ar: "ادفع بطريقتك",
    es: "Paga a tu manera",
    ne: "तपाईंको तरिकामा भुक्तान गर्नुहोस्",
    fr: "Payez à votre façon",
  },
  "feat.r3.p": {
    en: "Debit/credit cards or crypto — processed securely by certified third-party payment providers. We never see or store your full card details.",
    ru: "Карта, СБП или крипта — безопасно через сертифицированных платёжных провайдеров. Мы не видим полные данные карты и получаем только подтверждение.",
    fa: "کارت بانکی، یا رمزارز — با پردازش امن توسط تأمین‌کنندگان پرداخت معتبر شخص ثالث. ما هرگز جزئیات کامل کارت شما را نمی‌بینیم و ذخیره نمی‌کنیم.",
    ar: "بطاقة بنكية، أو عملات رقمية — تُعالج بأمان عبر مزودي دفع معتمدين من أطراف ثالثة. لا نرى ولا نخزن أبداً تفاصيل بطاقتك الكاملة.",
    es: "Tarjeta de débito/crédito o cripto — procesados de forma segura por proveedores de pago certificados de terceros. Nunca vemos ni almacenamos los datos completos de tu tarjeta.",
    ne: "डेबिट/क्रेडिट कार्ड वा क्रिप्टो — प्रमाणित तेस्रो-पक्ष भुक्तानी प्रदायकहरू मार्फत सुरक्षित रूपमा प्रशोधन। हामी तपाईंको कार्डको पूर्ण विवरण कहिल्यै हेर्दैनौं वा भण्डारण गर्दैनौं।",
    fr: "Carte bancaire ou crypto — traités en toute sécurité par des prestataires de paiement certifiés tiers. Nous ne voyons jamais et ne stockons jamais les données complètes de votre carte.",
  },
  "feat.tag4": {
    en: "Speed",
    ru: "Скорость",
    fa: "سرعت",
    ar: "السرعة",
    es: "Velocidad",
    ne: "गति",
    fr: "Vitesse",
  },
  "feat.r4.h": {
    en: "Fast enough for video calls",
    ru: "Достаточно быстрый для видеозвонков",
    fa: "به اندازه کافی سریع برای تماس‌های ویدیویی",
    ar: "سريع بما يكفي لمكالمات الفيديو",
    es: "Suficientemente rápido para videollamadas",
    ne: "भिडियो कलका लागि पर्याप्त छिटो",
    fr: "Assez rapide pour la visio",
  },
  "feat.r4.p": {
    en: "Premium European servers optimized for low latency across the EU, MENA, and South Asia. Streaming, video calls, and browsing at full speed.",
    ru: "Премиальные европейские серверы с низкой задержкой для ЕС, Ближнего Востока и Южной Азии. Стриминг, видеозвонки и браузинг на полной скорости.",
    fa: "سرورهای اروپایی برتر بهینه‌سازی‌شده برای تأخیر کم در اتحادیه اروپا، خاورمیانه و جنوب آسیا. استریم، تماس ویدیویی و مرور با سرعت کامل.",
    ar: "خوادم أوروبية متميزة محسّنة لزمن استجابة منخفض في أنحاء الاتحاد الأوروبي والشرق الأوسط وشمال إفريقيا وجنوب آسيا. بث ومكالمات فيديو وتصفح بأقصى سرعة.",
    es: "Servidores europeos premium optimizados para baja latencia en la UE, Oriente Medio y el sur de Asia. Streaming, videollamadas y navegación a plena velocidad.",
    ne: "युरोपेली प्रिमियम सर्भरहरू—EU, मध्य पूर्व र दक्षिण एसियाभर कम विलम्बनिताका लागि अनुकूलित। पूर्ण गतिमा स्ट्रिमिङ, भिडियो कल र ब्राउजिङ।",
    fr: "Serveurs européens premium optimisés pour une faible latence dans l’UE, au Moyen-Orient et en Asie du Sud. Streaming, visioconférences et navigation à pleine vitesse.",
  },
  "feat.tag5": {
    en: "Accessibility",
    ru: "Доступность",
    fa: "دسترسی‌پذیری",
    ar: "سهولة الوصول",
    es: "Accesibilidad",
    ne: "पहुँच",
    fr: "Accessibilité",
  },
  "feat.r5.h": {
    en: "Multiple ways to connect",
    ru: "Несколько способов подключения",
    fa: "روش‌های متعدد برای اتصال",
    ar: "طرق متعددة للاتصال",
    es: "Varias formas de conectarte",
    ne: "जडान गर्ने धेरै तरिकाहरू",
    fr: "Plusieurs façons de vous connecter",
  },
  "feat.r5.p": {
    en: "Android app for phones and tablets, plus a router application that protects every device on your home network — smart TVs, consoles, and IoT included.",
    ru: "Приложение для Android, а также роутер-приложение, защищающее все устройства домашней сети — ТВ, консоли и IoT включительно.",
    fa: "ربات تلگرام، اپلیکیشن اندروید، سایت Web2، یا TON Web3. اگر یک کانال مسدود شد، بقیه همچنان کار می‌کنند.",
    ar: "تطبيق أندرويد للهواتف والأجهزة اللوحية، إضافة إلى تطبيق راوتر يحمي كل جهاز في شبكتك المنزلية — شاشات ذكية وأجهزة ألعاب وأجهزة إنترنت الأشياء.",
    es: "App de Android para teléfonos y tabletas, más una aplicación para routers que protege cada dispositivo de tu red doméstica — televisores inteligentes, consolas e IoT incluidos.",
    ne: "Telegram बट, Android एप, Web2 साइट, वा TON Web3। यदि एक च्यानल असफल भयो भने, अरूहरू अझै काम गर्छन्।",
    fr: "Application Android pour téléphones et tablettes, plus une application routeur qui protège chaque appareil de votre réseau domestique — TV connectées, consoles et IoT inclus.",
  },
  "feat.cta.h": {
    en: "Ready to browse freely?",
    ru: "Готовы свободно сёрфить?",
    fa: "آماده مرور آزادانه هستید؟",
    ar: "جاهز للتصفح بحرية؟",
    es: "¿Listo para navegar libre?",
    ne: "स्वतन्त्र रूपमा ब्राउज गर्न तयार हुनुहुन्छ?",
    fr: "Prêt à naviguer librement ?",
  },
  "feat.cta.p": {
    en: "Join thousands of users already connected.",
    ru: "Присоединяйтесь к тысячам уже подключённых пользователей.",
    fa: "به هزاران کاربر که در حال حاضر متصل هستند بپیوندید.",
    ar: "انضم إلى آلاف المستخدمين المتصلين بالفعل.",
    es: "Únete a los miles de usuarios ya conectados.",
    ne: "पहिले नै जडान भएका हजारौं प्रयोगकर्ताहरूमा सामेल हुनुहोस्।",
    fr: "Rejoignez des milliers d'utilisateurs déjà connectés.",
  },
  "feat.cta.btn": {
    en: "See Pricing →",
    ru: "Смотреть цены →",
    fa: "مشاهده قیمت‌ها →",
    ar: "شاهد الأسعار →",
    es: "Ver precios →",
    ne: "मूल्य हेर्नुहोस् →",
    fr: "Voir les tarifs →",
  },
  "how.h1a": {
    en: "A secure tunnel,",
    ru: "Безопасный туннель,",
    fa: "VPN معمولی نیست.",
    ar: "نفق آمن،",
    es: "Un túnel seguro,",
    ne: "नियमित VPN होइन।",
    fr: "Un tunnel sécurisé,",
  },
  "how.h1b": {
    en: "not a shared VPN.",
    ru: "а не общий VPN.",
    fa: "اتصالی که فایروال‌ها نمی‌بینند.",
    ar: "لا VPN مشترك.",
    es: "no un VPN compartido.",
    ne: "निजी। एन्क्रिप्टेड। तपाईंको मात्र।",
    fr: "pas un VPN partagé.",
  },
  "how.sub": {
    en: "Up and running in 60 seconds. Here's how the technology actually works — and why it succeeds where other VPNs fail.",
    ru: "Запуск за 60 секунд. Как это устроено и почему работает там, где другие VPN не работают.",
    fa: "در ۶۰ ثانیه راه‌اندازی. فناوری چطور کار می‌کند و چرا جایی موفق است که VPNهای دیگر شکست می‌خورند.",
    ar: "جاهز خلال 60 ثانية. إليك كيف تعمل التقنية فعلًا — ولماذا تنجح حيث تفشل شبكات VPN الأخرى.",
    es: "Funcionando en 60 segundos. Así funciona la tecnología de verdad — y por qué tiene éxito donde otras VPN fallan.",
    ne: "६० सेकेन्डमा चालू। प्रविधि वास्तवमा कसरी काम गर्छ — र अरू VPN विफल हुँदा किन सफल हुन्छ।",
    fr: "Opérationnel en 60 secondes. Voici comment la technologie fonctionne réellement — et pourquoi elle réussit là où les autres VPN échouent.",
  },
  "how.optimise access.h": {
    en: "Built for difficult networks",
    ru: "Создан для сложных сетей",
    fa: "ساخته‌شده برای شبکه‌های دشوار",
    ar: "مصمّم للشبكات الصعبة",
    es: "Diseñado para redes difíciles",
    ne: "कठिन नेटवर्कका लागि बनाइएको",
    fr: "Conçu pour les réseaux difficiles",
  },
  "how.optimise access.lead": {
    en: "Traditional VPNs put many users behind one shared endpoint, which makes them crowded and inconsistent. NullVPN takes a fundamentally different approach: a private tunnel that belongs to you alone.",
    ru: "Традиционные VPN ставят множество пользователей за одну общую точку — отсюда перегрузка и нестабильность. NullVPN подходит иначе: приватный туннель, принадлежащий только вам.",
    fa: "بسیاری از VPNهای رایج کاربران زیادی را پشت یک نقطه اشتراکی قرار می‌دهند؛ نتیجه، شلوغی و عملکرد ناپایدار است. NullVPN رویکردی متفاوت دارد: تونل خصوصی که تنها به شما تعلق دارد.",
    ar: "تضع شبكات VPN التقليدية عددًا كبيرًا من المستخدمين خلف نقطة اتصال مشتركة واحدة، فتصبح مزدحمة وغير متسقة. يتبع NullVPN نهجًا مختلفًا جذريًا: نفق خاص يخصك وحدك.",
    es: "Many traditional VPNs rely on shared infrastructure that performs inconsistently under load. NullVPN takes a fundamentally different approach.",
    ne: "धेरै परम्परागत VPN ले धेरै प्रयोगकर्ताहरूलाई एउटै साझा अन्त्यबिन्दुपछि राख्छन्, जसले भीडभाड र अस्थिर प्रदर्शन निम्त्याउँछ। NullVPN को ठोस रूपमा फरक दृष्टिकोण छ: तपाईं आफैंमा मात्र समर्पित निजी टनल।",
    fr: "Many traditional VPNs rely on shared infrastructure that performs inconsistently under load. NullVPN takes a fundamentally different approach.",
  },
  "how.flow.h": {
    en: "Your connection experience",
    ru: "Как проходит подключение",
    fa: "تجربه اتصال شما",
    ar: "تجربة الاتصال",
    es: "Tu experiencia de conexión",
    ne: "तपाईंको जडान अनुभव",
    fr: "Votre expérience de connexion",
  },
  "how.steps.h": {
    en: "3 steps. 60 seconds.",
    ru: "3 шага. 60 секунд.",
    fa: "۳ قدم. ۶۰ ثانیه.",
    ar: "3 خطوات. 60 ثانية.",
    es: "3 pasos. 60 segundos.",
    ne: "३ कदम। ६० सेकेन्ड।",
    fr: "3 étapes. 60 secondes.",
  },
  "how.s1.h": {
    en: "Install the app",
    ru: "Установите приложение",
    fa: "اپلیکیشن را نصب کنید",
    ar: "ثبّت التطبيق",
    es: "Instala la app",
    ne: "एप इन्स्टल गर्नुहोस्",
    fr: "Installez l’application",
  },
  "how.s1.p": {
    en: "Get the APK directly from our website — no app store needed. It installs and configures itself silently.",
    ru: "Скачайте APK прямо с нашего сайта — магазин приложений не нужен. Установка и настройка проходят автоматически.",
    fa: "فایل APK را مستقیم از وب‌سایت ما بگیرید — بدون نیاز به استور. خودش نصب و تنظیم می‌شود.",
    ar: "احصل على ملف APK مباشرة من موقعنا — دون متجر تطبيقات. يثبّت ويضبط نفسه تلقائيًا.",
    es: "Descarga el APK directamente de nuestro sitio web — sin tienda de aplicaciones. Se instala y se configura solo.",
    ne: "APK सिधै हाम्रो वेबसाइटबाट लिनुहोस् — एप स्टोर आवश्यक छैन। यसले आफैँ इन्स्टल र कन्फिगर गर्छ।",
    fr: "Récupérez l’APK directement depuis notre site — sans store. Il s’installe et se configure tout seul.",
  },
  "how.s2.h": {
    en: "Tap Connect",
    ru: "Нажмите «Подключить»",
    fa: "روی «اتصال» بزنید",
    ar: "اضغط «اتصال»",
    es: "Toca «Conectar»",
    ne: "«जडान» थिच्नुहोस्",
    fr: "Touchez « Se connecter »",
  },
  "how.s2.p": {
    en: "Your personal connection is provisioned automatically. One tap and you’re online — free for the first 3 days.",
    ru: "Ваше персональное подключение создаётся автоматически. Одно касание — и вы онлайн. Первые 3 дня — бесплатно.",
    fa: "اتصال شخصی شما به‌صورت خودکار ساخته می‌شود. یک لمس و آنلاین می‌شوید — ۳ روز اول رایگان.",
    ar: "يُنشأ اتصالك الشخصي تلقائيًا. ضغطة واحدة وتكون متصلاً — أول 3 أيام مجانًا.",
    es: "Tu conexión personal se aprovisiona automáticamente. Un toque y estás en línea — los primeros 3 días gratis.",
    ne: "तपाईंको व्यक्तिगत जडान स्वतः तयार हुन्छ। एक थिचाइमा अनलाइन — पहिलो ३ दिन निःशुल्क।",
    fr: "Votre connexion personnelle est provisionnée automatiquement. Un geste et vous êtes en ligne — les 3 premiers jours sont gratuits.",
  },
  "how.s3.h": {
    en: "Pay when you’re ready",
    ru: "Оплатите, когда будете готовы",
    fa: "هر وقت آماده بودید پرداخت کنید",
    ar: "ادفع عندما تكون جاهزًا",
    es: "Paga cuando estés listo",
    ne: "तयार हुँदा तिर्नुहोस्",
    fr: "Payez quand vous êtes prêt",
  },
  "how.s3.p": {
    en: "After your 3 free days, pay with debit/credit cards or crypto (TON, USDT) via certified providers. A token arrives by e-mail for your other devices.",
    ru: "После 3 бесплатных дней оплатите картой или криптой (TON, USDT) через сертифицированных провайдеров. Токен для других устройств придёт на e-mail.",
    fa: "پس از ۳ روز رایگان، با کارت بانکی یا رمزارز (TON، USDT) از طریق ارائه‌دهندگان معتبر پرداخت کنید. توکن دستگاه‌های دیگر با ایمیل ارسال می‌شود.",
    ar: "بعد 3 أيام مجانية، ادفع ببطاقة بنكية أو عملات رقمية (TON، USDT) عبر مزوّدين معتمدين. يصلك رمز للأجهزة الأخرى عبر البريد الإلكتروني.",
    es: "Tras los 3 días gratis, paga con tarjeta de débito/crédito o cripto (TON, USDT) a través de proveedores certificados. El token para tus otros dispositivos llega por correo electrónico.",
    ne: "३ दिन निःशुल्क प्रयोगपछि, प्रमाणित प्रदायकहरूमार्फत डेबिट/क्रेडिट कार्ड वा क्रिप्टो (TON, USDT) बाट भुक्तानी गर्नुहोस्। अरू डिभाइसका लागि टोकन इमेलमा आउँछ।",
    fr: "Après vos 3 jours gratuits, payez par carte bancaire ou en crypto (TON, USDT) via des prestataires certifiés. Un jeton pour vos autres appareils arrive par e-mail.",
  },
  "how.note1.h": {
    en: "🔒 What happens to your data?",
    ru: "🔒 Что происходит с вашими данными?",
    fa: "🔒 با داده‌های شما چه اتفاقی می‌افتد؟",
    ar: "🔒 ماذا يحدث لبياناتك؟",
    es: "🔒 ¿Qué pasa con tus datos?",
    ne: "🔒 तपाईंको डेटाको के हुन्छ?",
    fr: "🔒 Que deviennent vos données ?",
  },
  "how.note1.p": {
    en: "Your browsing content is never stored — it passes through your tunnel encrypted, end to end. We keep only minimal operational data needed to run the service (such as approximate data volume per billing period), and nothing that links your identity to the sites you visit.",
    ru: "Содержимое вашего трафика никогда не хранится — оно идёт по туннелю в шифровании end-to-end. Мы храним только минимальные операционные данные для работы сервиса (например, примерный объём трафика за период), и ничего, что связывало бы вас с посещаемыми сайтами.",
    fa: "محتوای مرور شما هرگز ذخیره نمی‌شود — از طریق تونل شما رمزنگاری‌شده و سرتاسری عبور می‌کند. ما فقط حداقل داده‌های عملیاتی لازم برای اداره سرویس را نگه می‌داریم (مثلاً حجم تقریبی داده در هر دوره صورتحساب)، و هیچ چیزی که هویت شما را به سایت‌های بازدیدشده پیوند دهد.",
    ar: "لا يتم تخزين محتوى تصفحك أبدًا — يمر عبر نفقك مشفرًا من الطرف إلى الطرف. نحتفظ فقط بالحد الأدنى من البيانات التشغيلية اللازمة لتشغيل الخدمة (مثل حجم البيانات التقريبي لكل فترة فوترة)، ولا شيء يربط هويتك بالمواقع التي تزورها.",
    es: "El contenido de tu navegación nunca se almacena — pasa por tu túnel cifrado de extremo a extremo. Solo conservamos los datos operativos mínimos necesarios para operar el servicio (como el volumen aproximado de datos por periodo de facturación), y nada que vincule tu identidad con los sitios que visitas.",
    ne: "तपाईंको ब्राउजिङ सामग्री कहिल्यै भण्डारण गरिँदैन — यो तपाईंको टनलबाट इन्क्रिप्टेड, अन्त्यदेखि-अन्त्यसम्म प्रवाह हुन्छ। हामी सेवा सञ्चालनका लागि चाहिने न्यूनतम परिचालन डाटा मात्र राख्छौं (जस्तै प्रति बिलिङ अवधि अनुमानित डाटा मात्रा), र तपाईंको पहिचानलाई भ्रमण गरिएका साइटहरूसँग जोड्ने कुनै चीज होइन।",
    fr: "Le contenu de votre navigation n'est jamais stocké — il passe par votre tunnel chiffré, de bout en bout. Nous ne conservons que les données opérationnelles minimales nécessaires au service (comme le volume de données approximatif par période de facturation), et rien qui relie votre identité aux sites que vous visitez.",
  },
  "how.note2.h": {
    en: "📱 Which devices are supported?",
    ru: "📱 Какие устройства поддерживаются?",
    fa: "📱 کدام دستگاه‌ها پشتیبانی می‌شوند؟",
    ar: "📱 ما الأجهزة المدعومة؟",
    es: "📱 ¿Qué dispositivos son compatibles?",
    ne: "📱 कुन उपकरणहरू समर्थित छन्?",
    fr: "📱 Quels appareils sont pris en charge ?",
  },
  "how.note2.p": {
    en: "Android phones and tablets with our dedicated app, routers running our custom firmware, and other devices via standard configuration files — full instructions provided after purchase.",
    ru: "Телефоны и планшеты Android с нашим приложением, роутеры с нашей прошивкой и другие устройства через стандартные конфигурации — инструкции после покупки.",
    fa: "گوشی‌ها و تبلت‌های اندرویدی با اپ اختصاصی ما، روترهای دارای فریمور اختصاصی ما، و سایر دستگاه‌ها از طریق فایل‌های پیکربندی استاندارد — راهنمای کامل پس از خرید ارائه می‌شود.",
    ar: "هواتف وأجهزة لوحية بأندرويد عبر تطبيقنا المخصص، وأجهزة راوتر تعمل بنظامنا المخصص، وأجهزة أخرى عبر ملفات إعداد قياسية — الإرشادات الكاملة تُقدَّم بعد الشراء.",
    es: "Teléfonos y tabletas Android con nuestra aplicación dedicada, routers con nuestro firmware propio y otros dispositivos mediante archivos de configuración estándar — instrucciones completas tras la compra.",
    ne: "हाम्रो समर्पित एपसहित एन्ड्रोइड फोन र ट्याब्लेट, हाम्रो अनुकूलित फर्मवेयर चल्ने राउटरहरू, र अन्य उपकरणहरू मानक कन्फिगरेसन फाइलमार्फत — खरिदपछि पूर्ण निर्देशन उपलब्ध हुन्छ।",
    fr: "Téléphones et tablettes Android avec notre application dédiée, routeurs avec notre firmware personnalisé, et autres appareils via des fichiers de configuration standard — instructions complètes fournies après l'achat.",
  },
  "how.note3.h": {
    en: "🔄 What if a connection path fails?",
    ru: "🔄 Что если одно из направлений станет недоступно?",
    fa: "🔄 اگر یک مسیر در دسترس نباشد چه؟",
    ar: "🔄 ماذا لو تعطل مسار الاتصال؟",
    es: "🔄 ¿Y si una ruta de conexión falla?",
    ne: "🔄 जडान असफल भएमा के हुन्छ?",
    fr: "🔄 Et si une route de connexion échoue ?",
  },
  "how.note3.p": {
    en: "NullVPN includes automatic backup paths. If one route becomes unavailable, your tunnel can switch to another one. If you experience any issues, message <a href=\"https://t.me/nullvpn_net\" target=\"_blank\" rel=\"noopener\" referrerpolicy=\"no-referrer\">@nullvpn_net</a> on Telegram.",
    ru: "В NullVPN есть автоматические резервные маршруты. Если одно направление становится недоступным, туннель может переключиться на другое. Возникли проблемы? Напишите <a href=\"https://t.me/nullvpn_net\" target=\"_blank\" rel=\"noopener\" referrerpolicy=\"no-referrer\">@nullvpn_net</a> в Telegram.",
    fa: "NullVPN مسیرهای پشتیبان خودکار دارد. اگر یک مسیر در دسترس نباشد، تونل شما می‌تواند به مسیر دیگری سوئیچ کند. اگر مشکلی پیش آمد، در تلگرام به <a href=\"https://t.me/nullvpn_net\" target=\"_blank\" rel=\"noopener\" referrerpolicy=\"no-referrer\">@nullvpn_net</a> پیام بدهید.",
    ar: "يتضمن NullVPN مسارات احتياطية تلقائية. إذا أصبح أحد المسارات غير متاح، يمكن لنفقك التبديل إلى مسار آخر. إذا واجهت أي مشكلة، راسل <a href=\"https://t.me/nullvpn_net\" target=\"_blank\" rel=\"noopener\" referrerpolicy=\"no-referrer\">@nullvpn_net</a> على تيليجرام.",
    es: "NullVPN incluye rutas de respaldo automáticas. Si una ruta deja de estar disponible, tu túnel puede cambiar a otra. Si tienes algún problema, escribe a <a href=\"https://t.me/nullvpn_net\" target=\"_blank\" rel=\"noopener\" referrerpolicy=\"no-referrer\">@nullvpn_net</a> en Telegram.",
    ne: "NullVPN मा स्वतः ब्याकअप मार्गहरू छन्। एउटा मार्ग अनुपलब्ध भएमा, तपाईंको टनल अर्कोमा स्विच गर्न सक्छ। कुनै समस्या भएमा, Telegram मा <a href=\"https://t.me/nullvpn_net\" target=\"_blank\" rel=\"noopener\" referrerpolicy=\"no-referrer\">@nullvpn_net</a> लाई सन्देश पठाउनुहोस्।",
    fr: "NullVPN intègre des chemins de secours automatiques. Si une route devient indisponible, votre tunnel peut en emprunter une autre. En cas de problème, écrivez à <a href=\"https://t.me/nullvpn_net\" target=\"_blank\" rel=\"noopener\" referrerpolicy=\"no-referrer\">@nullvpn_net</a> sur Telegram.",
  },
  "how.note4.h": {
    en: "🌐 Where else can you reach us?",
    ru: "🌐 Где нас ещё найти?",
    fa: "🌐 اگر این وب‌سایت مسدود باشد چه؟",
    ar: "🌐 أين تجدنا غير هنا؟",
    es: "🌐 ¿Dónde más puedes contactarnos?",
    ne: "🌐 यदि यो वेबसाइट असफल भएमा के हुन्छ?",
    fr: "🌐 Comment nous joindre ailleurs ?",
  },
  "how.note4.p": {
    en: "Reach us via <a href=\"https://t.me/nullvpnnetbot\" target=\"_blank\" rel=\"noopener\" referrerpolicy=\"no-referrer\">@nullvpnnetbot</a> on Telegram or via <a href=\"web3.html\" target=\"_blank\" rel=\"noopener\" referrerpolicy=\"no-referrer\">our TON Web3 page</a> — works in any browser, no special software needed.",
    ru: "Свяжитесь через <a href=\"https://t.me/nullvpnnetbot\" target=\"_blank\" rel=\"noopener\" referrerpolicy=\"no-referrer\">@nullvpnnetbot</a> в Telegram или через <a href=\"web3.html\" target=\"_blank\" rel=\"noopener\" referrerpolicy=\"no-referrer\">нашу страницу TON Web3</a> — работает в любом браузере.",
    fa: "از <a href=\"https://t.me/nullvpnnetbot\" target=\"_blank\" rel=\"noopener\" referrerpolicy=\"no-referrer\">@nullvpnnetbot</a> در تلگرام یا از طریق <a href=\"web3.html\" target=\"_blank\" rel=\"noopener\" referrerpolicy=\"no-referrer\">صفحهٔ TON Web3</a> با ما تماس بگیرید — در هر مرورگر کار می‌کند.",
    ar: "تواصل معنا عبر <a href=\"https://t.me/nullvpnnetbot\" target=\"_blank\" rel=\"noopener\" referrerpolicy=\"no-referrer\">@nullvpnnetbot</a> على Telegram أو عبر <a href=\"web3.html\" target=\"_blank\" rel=\"noopener\" referrerpolicy=\"no-referrer\">صفحتنا على TON Web3</a> — تعمل في أي متصفح دون برمجيات خاصة.",
    es: "Contáctanos vía <a href=\"https://t.me/nullvpnnetbot\" target=\"_blank\" rel=\"noopener\" referrerpolicy=\"no-referrer\">@nullvpnnetbot</a> en Telegram o vía <a href=\"web3.html\" target=\"_blank\" rel=\"noopener\" referrerpolicy=\"no-referrer\">nuestra página TON Web3</a> — funciona en cualquier navegador, sin software especial.",
    ne: "Telegram मा <a href=\"https://t.me/nullvpnnetbot\" target=\"_blank\" rel=\"noopener\" referrerpolicy=\"no-referrer\">@nullvpnnetbot</a> वा <a href=\"web3.html\" target=\"_blank\" rel=\"noopener\" referrerpolicy=\"no-referrer\">हाम्रो TON Web3 पृष्ठ</a> मा हामीलाई सम्पर्क गर्नुहोस् — कुनै पनि ब्राउजरमा काम गर्छ।",
    fr: "Joignez-nous via <a href=\"https://t.me/nullvpnnetbot\" target=\"_blank\" rel=\"noopener\" referrerpolicy=\"no-referrer\">@nullvpnnetbot</a> sur Telegram ou via <a href=\"web3.html\" target=\"_blank\" rel=\"noopener\" referrerpolicy=\"no-referrer\">notre page TON Web3</a> — accessible depuis n'importe quel navigateur, sans logiciel particulier.",
  },
  "how.cta.h": {
    en: "Ready to connect?",
    ru: "Готовы подключиться?",
    fa: "آماده اتصال هستید؟",
    ar: "جاهز للاتصال؟",
    es: "¿Listo para conectarte?",
    ne: "जडान गर्न तयार हुनुहुन्छ?",
    fr: "Prêt à vous connecter ?",
  },
  "how.cta.p": {
    en: "From $3/month. Cancel anytime. Works in 60 seconds.",
    ru: "От 300 ₽/мес. Отмена в любое время. Работает за 60 секунд.",
    fa: "از ۳ دلار/ماه. هر زمان لغو. ۶۰ ثانیه‌ای کار می‌کند.",
    ar: "ابتداءً من $3 شهريًا. ألغِ متى شئت. جاهز خلال 60 ثانية.",
    es: "Desde $3/mes. Cancela cuando quieras. Listo en 60 segundos.",
    ne: "$3/महिनाबाट। जुनसुकै समय रद्द। ६० सेकेन्डमा काम गर्छ।",
    fr: "Dès $3/mois. Résiliable à tout moment. Opérationnel en 60 secondes.",
  },
  "how.cta.btn": {
    en: "See Pricing →",
    ru: "Смотреть цены →",
    fa: "مشاهده قیمت‌ها →",
    ar: "شاهد الأسعار →",
    es: "Ver precios →",
    ne: "मूल्य हेर्नुहोस् →",
    fr: "Voir les tarifs →",
  },
  "how.cta.small": {
    en: "See how NullVPN compares to NordVPN, ExpressVPN, ProtonVPN →",
    ru: "Сравнение NullVPN с NordVPN, ExpressVPN, ProtonVPN →",
    fa: "مقایسه NullVPN با NordVPN، ExpressVPN، ProtonVPN →",
    ar: "شاهد كيف يقارن NullVPN مع NordVPN وExpressVPN وProtonVPN →",
    es: "Mira cómo se compara NullVPN con NordVPN, ExpressVPN y ProtonVPN →",
    ne: "NullVPN को NordVPN, ExpressVPN, ProtonVPN सँग तुलना हेर्नुहोस् →",
    fr: "Voir comment NullVPN se compare à NordVPN, ExpressVPN et ProtonVPN →",
  },
  "how.regular.h": {
    en: "❌ Regular VPNs",
    ru: "❌ Обычные VPN",
    fa: "❌ VPNهای معمولی",
    ar: "❌ شبكات VPN التقليدية",
    es: "❌ VPN comunes",
    ne: "❌ नियमित VPN",
    fr: "❌ VPN ordinaires",
  },
  "how.regular.1": {
    en: "Route everyone through the same shared endpoints",
    ru: "Ставят всех пользователей на общие перегруженные точки",
    fa: "از الگوهای اتصال به‌راحتی قابل شناسایی استفاده می‌کنند",
    ar: "تمرر الجميع عبر نقاط الاتصال المشتركة نفسها",
    es: "Usan patrones de conexión fácilmente disruptives",
    ne: "भीडभाड भएको साझा एन्डपोइन्टमा भर पर्छन्",
    fr: "Utilisent des schémas de connexion facilement détectables",
  },
  "how.regular.2": {
    en: "Predictable, single-path connections",
    ru: "Один маршрут без запасного варианта",
    fa: "اتصال‌های تک‌مسیره و قابل پیش‌بینی",
    ar: "اتصالات أحادية المسار يمكن التنبؤ بها",
    es: "Conexiones de ruta única y predecibles",
    ne: "एउटा मात्र बाटो, कुनै विकल्प छैन",
    fr: "Connexions à chemin unique, prévisibles",
  },
  "how.regular.3": {
    en: "Crowded servers degrade speed and stability",
    ru: "Общие диапазоны адресов работают нестабильно",
    fa: "اثر ترافیکی قابل شناسایی به جا می‌گذارند",
    ar: "الخوادم المزدحمة تُضعف السرعة والاستقرار",
    es: "Los servidores saturados degradan velocidad y estabilidad",
    ne: "साझा ठेगाना दायरा अस्थिर प्रदर्शन",
    fr: "Les serveurs surchargés dégradent vitesse et stabilité",
  },
  "how.regular.4": {
    en: "Shared address ranges that perform inconsistently",
    ru: "Перегруженные серверы снижают скорость и стабильность",
    fa: "محدوده IP عمومی فهرست شده — مداوم بلاک می‌شود",
    ar: "نطاقات عناوين مشتركة بأداء متقلب",
    es: "Rangos de direcciones compartidos con rendimiento inconsistente",
    ne: "भीडभाड सर्भरले गति र स्थिरता घटाउँछ",
    fr: "Plages d'adresses partagées aux performances irrégulières",
  },
  "how.regular.5": {
    en: "Require app store installation",
    ru: "Требуют установки из магазина приложений",
    fa: "نیاز به نصب از فروشگاه اپ دارند",
    ar: "تتطلب متجر تطبيقات",
    es: "Requieren tienda de aplicaciones",
    ne: "एप स्टोर इन्स्टलेसन आवश्यक छ",
    fr: "Exigent un magasin d'applications",
  },
  "how.regular.verdict": {
    en: "Result: inconsistent performance on demanding networks",
    ru: "Итог: нестабильная работа в сложных сетях",
    fa: "نتیجه: مسدود در شبکه‌های محدود در عرض چند روز",
    ar: "النتيجة: أداء غير متسق على الشبكات المتطلبة",
    es: "Resultado: rendimiento inconsistente en redes exigentes",
    ne: "नतिजा: प्रतिबन्धित सञ्जालहरूमा केही दिनमा असंगत",
    fr: "Résultat : performances irrégulières sur les réseaux exigeants",
  },
  "how.nullvpn.h": {
    en: "✅ NullVPN",
    ru: "✅ NullVPN",
    fa: "✅ NullVPN",
    ar: "✅ NullVPN",
    es: "✅ NullVPN",
    ne: "✅ NullVPN",
    fr: "✅ NullVPN",
  },
  "how.nullvpn.1": {
    en: "A private tunnel dedicated to you",
    ru: "Приватный туннель, выделенный только вам",
    fa: "یک تونل خصوصی مخصوص شما",
    ar: "نفق خاص مخصص لك وحدك",
    es: "Un túnel privado dedicado a ti",
    ne: "तपाईंका लागि समर्पित निजी टनेल",
    fr: "Un tunnel privé qui vous est dédié",
  },
  "how.nullvpn.2": {
    en: "Traffic encrypted end-to-end, from your device outward",
    ru: "Трафик шифруется end-to-end, от вашего устройства",
    fa: "ترافیک از دستگاه شما تا مقصد رمزنگاری می​شود",
    ar: "بيانات مشفرة من طرف إلى طرف، من جهازك outward",
    es: "Tráfico cifrado de extremo a extremo, desde tu dispositivo hacia afuera",
    ne: "ट्राफिक तपाईंको यन्त्रबाट एन्क्रिप्ट हुन्छ",
    fr: "Trafic chiffré de bout en bout, depuis votre appareil",
  },
  "how.nullvpn.3": {
    en: "No shared-server congestion — performance is yours alone",
    ru: "Никакой перегрузки общих серверов",
    fa: "بدون ازدحام سرور مشترک",
    ar: "لا ازدحام خوادم مشتركة — الأداء لك وحدك",
    es: "Sin congestión de servidores compartidos — el rendimiento es solo tuyo",
    ne: "कुनै साझा सर्भर भीड छैन",
    fr: "Aucune congestion de serveurs partagés — la performance n'appartient qu'à vous",
  },
  "how.nullvpn.4": {
    en: "Multiple independent encryption layers",
    ru: "Несколько независимых слоёв шифрования",
    fa: "لایه‌های رمزنگاری مستقل متعدد",
    ar: "طبقات تشفير مستقلة متعددة",
    es: "Múltiples capas independientes de cifrado",
    ne: "धेरै स्वतन्त्र इन्क्रिप्सन तहहरू",
    fr: "Plusieurs couches de chiffrement indépendantes",
  },
  "how.nullvpn.5": {
    en: "Automatic switching to the best working path",
    ru: "Авто-переключение на рабочий маршрут",
    fa: "سوئیچ خودکار به بهترین مسیر فعال",
    ar: "تبديل تلقائي إلى أفضل مسار متاح",
    es: "Cambio automático a la mejor ruta disponible",
    ne: "उपलब्ध उत्तम मार्गमा स्वतः स्विच",
    fr: "Bascule automatique vers la meilleure route disponible",
  },
  "how.nullvpn.6": {
    en: "No app store required — direct APK",
    ru: "Без магазина приложений — прямая APK",
    fa: "بدون نیاز به فروشگاه اپ — APK مستقیم",
    ar: "بلا متجر تطبيقات — APK مباشر",
    es: "Sin tienda de aplicaciones — APK directo",
    ne: "कुनै एप स्टोर आवश्यक छैन — प्रत्यक्ष APK",
    fr: "Sans magasin d'applications — APK direct",
  },
  "how.nullvpn.verdict": {
    en: "✅ Works on corporate, mobile, fixed, and public networks",
    ru: "✅ Работает в корпоративных, мобильных, домашних и публичных сетях",
    fa: "✅ روی شبکه‌های سازمانی، موبایل، ثابت و عمومی کار می‌کند",
    ar: "✅ يعمل على الشبكات المؤسسية والجوال والثابتة والعامة",
    es: "✅ Funciona en redes corporativas, móviles, fijas y públicas",
    ne: "✅ कम्पनी, मोबाइल, स्थिर र सार्वजनिक सञ्जालहरूमा काम गर्छ",
    fr: "✅ Fonctionne sur les réseaux d’entreprise, mobiles, fixes et publics",
  },
  "how.analogy.h": {
    en: "The Simple Analogy",
    ru: "Простая аналогия",
    fa: "تشبیه ساده",
    ar: "التشبيه البسيط",
    es: "La analogía simple",
    ne: "साधारण उपमा",
    fr: "L'analogie simple",
  },
  "how.analogy.p1": {
    en: "Shared VPN servers are like a single busy entrance for an entire building — crowded, unpredictable, and one closed door locks everyone out.",
    ru: "Общие VPN-серверы — как один вход на весь жилой дом: толпа, непредсказуемость, и закрытая дверь запирает всех.",
    fa: "سرورهای VPN مشترک مثل یک ورودی شلوغ برای کل یک ساختمان هستند — شلوغ، غیرقابل‌پیش‌بینی، و یک درِ بسته همه را بیرون قفل می‌کند.",
    ar: "خوادم VPN المشتركة كمدخل واحد مزدحم لمبنى كامل — مزدحمة، يصعب التنبؤ بها، وباب واحد مغلق يقفل الجميع في الخارج.",
    es: "Los servidores VPN compartidos son como una única entrada concurrida para todo un edificio: llena, impredecible, y una puerta cerrada deja a todos afuera.",
    ne: "साझा VPN सर्भरहरू पूरै भवनको एउटा व्यस्त प्रवेशद्वार जस्तै हुन् — भीडभाड, अप्रत्याशित, र एउटा बन्द ढोकाले सबैलाई बाहिर थुन्छ।",
    fr: "Les serveurs VPN partagés ressemblent à une entrée unique et bondée pour tout un immeuble — bondée, imprévisible, et une porte fermée enferme tout le monde dehors.",
  },
  "how.analogy.p2": {
    en: "NullVPN gives every user a private entrance on a common, well-maintained road. It's direct, it's encrypted, and closing one path never affects anyone else.",
    ru: "NullVPN даёт каждому пользователю отдельный вход на общей ухоженной дороге. Он прямой, зашифрованный, и закрытие одного пути не затрагивает других.",
    fa: "NullVPN به هر کاربر یک ورودی خصوصی روی یک جادهٔ مشترک و خوش‌مدیریت می‌دهد. مستقیم است، رمزنگاری‌شده است، و بستن یک مسیر هرگز روی دیگران اثر نمی‌گذارد.",
    ar: "يمنح NullVPN كل مستخدم مدخلاً خاصاً على طريق عام جيد الصيانة. إنه مباشر ومشفّر، وإغلاق مسير واحد لا يؤثر على أي شخص آخر.",
    es: "NullVPN da a cada usuario una entrada privada en una vía común y bien cuidada. Es directa, está cifrada y cerrar un camino nunca afecta a los demás.",
    ne: "NullVPN ले प्रत्येक प्रयोगकर्तालाई साझा, राम्रोसँग मर्मत गरिएको सडकमा निजी प्रवेशद्वार दिन्छ। यो सिधा छ, इन्क्रिप्टेड छ, र एउटा मार्ग बन्द हुँदा अरूलाई कहिल्यै असर पर्दैन।",
    fr: "NullVPN offre à chaque utilisateur une entrée privée sur une route commune bien entretenue. Elle est directe, chiffrée, et la fermeture d'un chemin n'affecte jamais personne d'autre.",
  },
  "how.port.h": {
    en: "Engineered for Reliability",
    ru: "Спроектирован для надёжности",
    fa: "مهندسی‌شده برای پایداری",
    ar: "مصمم للموثوقية",
    es: "Diseñado para la fiabilidad",
    ne: "भरपर्दोपनका लागि डिजाइन",
    fr: "Conçu pour la fiabilité",
  },
  "how.port.p": {
    en: "NullVPN operates over the standard port used by every secure website on the internet — banking, healthcare, retail. Because these paths carry ordinary encrypted traffic, they stay open and fast everywhere.",
    ru: "NullVPN работает на стандартном порту, который используют все защищённые сайты интернета — банки, медицина, торговля. По этим путям идёт обычный шифрованный трафик, поэтому они остаются открытыми и быстрыми везде.",
    fa: "NullVPN از همان درگاه استانداردی استفاده می‌کند که هر وب‌سایت امن اینترنت — بانکداری، درمان، خرده‌فروشی — به کار می‌برد. چون این مسیرها ترافیک رمزنگاری‌شده معمولی را جابه‌جا می‌کنند، همه‌جا باز و سریع می‌مانند.",
    ar: "يعمل NullVPN عبر المنفذ القياسي الذي تستخدمه كل المواقع الآمنة على الإنترنت — البنوك والصحة والتجزئة. ولأن هذه المسارات تنقل بيانات مشفرة عادية، تبقى مفتوحة وسريعة في كل مكان.",
    es: "NullVPN opera sobre el puerto estándar que usa todo sitio web seguro de internet — banca, salud, comercio. Como esas rutas llevan tráfico cifrado ordinario, permanecen abiertas y rápidas en todas partes.",
    ne: "NullVPN इन्टरनेटमा हरेक सुरक्षित वेबसाइटले प्रयोग गर्ने मानक पोर्टमा सञ्चालन हुन्छ — बैंकिङ, स्वास्थ्य देखाउने, खुद्रा व्यापार। यी पथहरू सामान्य इन्क्रिप्टेड ट्राफिक बोक्ने हुनाले, तिनीहरू हर ठाउँमा खुला र छिटो बनिरहन्छन्।",
    fr: "NullVPN emprunte le port standard utilisé par chaque site web sécurisé d'Internet — banque, santé, commerce. Comme ces routes transportent du trafic chiffré ordinaire, elles restent ouvertes et rapides partout.",
  },
  "how.tech.h": {
    en: "Technology at a glance",
    ru: "Технология вкратце",
    fa: "فناوری در یک نگاه",
    ar: "التقنية في لمحة",
    es: "La tecnología de un vistazo",
    ne: "प्रविधि एक नजरमा",
    fr: "La technologie en un coup d'œil",
  },
  "how.tech.1": {
    en: "A private tunnel with dedicated endpoints — never shared crowds",
    ru: "Приватный туннель с выделенными точками выхода — никогда не общий",
    fa: "تونل شخصی با نقاط اتصال اختصاصی — بدون شلوغی مشترک",
    ar: "نفق خاص بنقاط اتصال مخصصة — لا ازدحام مشترك أبدًا",
    es: "Un túnel privado con puntos de conexión dedicados — nunca multitudes compartidas",
    ne: "डिडिकेटेड जडान बिन्दुसँग एउटा व्यक्तिगत टनेल — कहिल्यै साझा भीड हुँदैन",
    fr: "Un tunnel privé avec des points de connexion dédiés — jamais la foule partagée",
  },
  "how.tech.2": {
    en: "Minimal connection metadata — connection details are kept private by design to protect the integrity of our service",
    ru: "Минимальный отпечаток трафика — детали соединения закрыты по дизайну для защиты целостности сервиса",
    fa: "اثر حداقلی ترافیک — جزئیات اتصال محرمانه می‌ماند تا یکپارچگی سرویس حفظ شود",
    ar: "بيانات وصفية دنيا للاتصال — تُبقى تفاصيل الاتصال خاصة بالتصميم لحماية سلامة خدمتنا",
    es: "Huella de tráfico mínima: los detalles de la conexión se mantienen privados por diseño para proteger la integridad del servicio",
    ne: "न्यूनतम ट्राफिक फिंगरप्रिन्ट—सेवाको अखण्डता जोगाउन जडान विवरण निजी राखिन्छ",
    fr: "Empreinte de trafic minimale : les détails de connexion restent privés par conception, pour protéger l’intégrité du service",
  },
  "how.tech.3": {
    en: "Multiple independent military-grade encryption layers",
    ru: "Несколько независимых слоёв шифрования военного уровня",
    fa: "لایه‌های رمزنگاری مستقل متعدد در سطح نظامی",
    ar: "طبقات تشفير مستقلة متعددة بمستوى عسكري",
    es: "Múltiples capas independientes de cifrado de grado militar",
    ne: "धेरै स्वतन्त्र सैन्य-ग्रेड इन्क्रिप्सन तहहरू",
    fr: "Plusieurs couches indépendantes de chiffrement de niveau militaire",
  },
  "how.tech.4": {
    en: "Automatic backup routes — other paths ready if one is unavailable",
    ru: "Автоматические резервные маршруты — есть альтернатива, если один путь недоступен",
    fa: "مسیرهای پشتیبان خودکار — اگر یکی در دسترس نباشد، مسیرهای دیگری آماده‌اند",
    ar: "مسارات احتياطية تلقائية — مسارات أخرى جاهزة إذا تعذر أحدها",
    es: "Rutas de respaldo automáticas — otras rutas listas si una no está disponible",
    ne: "स्वतः ब्याकअप मार्गहरू — एउटा अनुपलब्ध भएमा अरू मार्गहरू तयार",
    fr: "Routes de secours automatiques — d'autres routes prêtes si l'une est indisponible",
  },
  "how.tech.5": {
    en: "Dedicated private server — only your traffic, ever",
    ru: "Выделенный приватный сервер — только ваш трафик, всегда",
    fa: "سرور خصوصی اختصاصی — فقط ترافیک شما، همیشه",
    ar: "خادم خاص مخصص — بياناتك وحدك، دائمًا",
    es: "Servidor privado dedicado — solo tu tráfico, siempre",
    ne: "समर्पित निजी सर्भर — केवल तपाईंको ट्राफिक, सधैं",
    fr: "Serveur privé dédié — uniquement votre trafic, toujours",
  },
  "how.tech.6": {
    en: "No activity logs by architecture, not just policy",
    ru: "Отсутствие логов активности по архитектуре, а не просто по политике",
    fa: "بدون گزارش فعالیت توسط معماری، نه فقط سیاست",
    ar: "بلا سجلات نشاط بنيويًا، لا سياسة فقط",
    es: "Sin registros de actividad por arquitectura, no solo por política",
    ne: "वास्तुकला द्वारा कुनै गतिविधि लगहरू, केवल नीति होइन",
    fr: "Aucun journal d'activité par architecture, pas seulement par politique",
  },
  "how.flow.1": {
    en: "Tap to install",
    ru: "Нажмите для установки",
    fa: "برای نصب ضربه بزنید",
    ar: "اضغط للتثبيت",
    es: "Toca para instalar",
    ne: "इन्स्टल गर्न ट्याप गर्नुहोस्",
    fr: "Touchez pour installer",
  },
  "how.flow.1.d": {
    en: "The APK installs and configures itself silently — no manual setup.",
    ru: "APK устанавливается и настраивается сам — вручную делать ничего не нужно.",
    fa: "فایل APK خودش نصب و پیکربندی می‌شود — بدون تنظیم دستی.",
    ar: "يُثبَّت ملف APK ويضبط نفسه تلقائيًا — دون أي إعداد يدوي.",
    es: "El APK se instala y se configura solo, en silencio — sin pasos manuales.",
    ne: "APK ले आफैँ इन्स्टल र कन्फिगर गर्छ — म्यानुअल सेटअप आवश्यक पर्दैन।",
    fr: "L’APK s’installe et se configure tout seul, en silence — aucun réglage manuel.",
  },
  "how.flow.2": {
    en: "Auto-provisioned",
    ru: "Автоматическая настройка",
    fa: "تهیه خودکار",
    ar: "تجهيز تلقائي",
    es: "Configuración automática",
    ne: "स्वतः सेटअप",
    fr: "Configuration automatique",
  },
  "how.flow.2.d": {
    en: "The system generates your personal connection instantly.",
    ru: "Система мгновенно создаёт ваше персональное подключение.",
    fa: "سامانه بی‌درنگ اتصال شخصی شما را می‌سازد.",
    ar: "ينشئ النظام اتصالك الشخصي فورًا.",
    es: "El sistema genera tu conexión personal al instante.",
    ne: "प्रणालीले तपाईंको व्यक्तिगत जडान तुरुन्तै बनाउँछ।",
    fr: "Le système génère votre connexion personnelle instantanément.",
  },
  "how.flow.3": {
    en: "Connected",
    ru: "Вы подключены",
    fa: "متصل شدید",
    ar: "أنت متصل",
    es: "Conectado",
    ne: "जडान भयो",
    fr: "Connecté",
  },
  "how.flow.3.d": {
    en: "Tap Connect — you’re online.",
    ru: "Нажмите «Подключить» — и вы онлайн.",
    fa: "روی «اتصال» بزنید — آنلاین می‌شوید.",
    ar: "اضغط «اتصال» — وأنت متصل الآن.",
    es: "Toca «Conectar» — ya estás en línea.",
    ne: "«जडान» थिच्नुहोस् — अब तपाईं अनलाइन हुनुहुन्छ।",
    fr: "Touchez « Se connecter » — vous êtes en ligne.",
  },
  "how.flow.4": {
    en: "3 days free",
    ru: "3 дня бесплатно",
    fa: "۳ روز رایگان",
    ar: "3 أيام مجانية",
    es: "3 días gratis",
    ne: "३ दिन निःशुल्क",
    fr: "3 jours gratuits",
  },
  "how.flow.4.d": {
    en: "You try NullVPN free for 3 days.",
    ru: "Первые 3 дня NullVPN — бесплатно.",
    fa: "۳ روز NullVPN را رایگان امتحان کنید.",
    ar: "جرّب NullVPN مجانًا لمدة 3 أيام.",
    es: "Prueba NullVPN gratis durante 3 días.",
    ne: "३ दिनसम्म NullVPN निःशुल्क प्रयोग गर्नुहोस्।",
    fr: "Essayez NullVPN gratuitement pendant 3 jours.",
  },
  "how.flow.5": {
    en: "You pay",
    ru: "Вы оплачиваете",
    fa: "پرداخت شما",
    ar: "تدفع ثمن اشتراكك",
    es: "Realizas el pago",
    ne: "तपाईं भुक्तानी गर्नुहुन्छ",
    fr: "Vous payez",
  },
  "how.flow.5.d": {
    en: "Debit/credit cards or crypto (TON, USDT) — payments are handled by certified providers.",
    ru: "Карта, СБП или криптовалюта (TON, USDT) — платёж проводят сертифицированные провайдеры.",
    fa: "کارت بانکی یا رمزارز (TON و USDT) — پرداخت توسط ارائه‌دهندگان مجاز انجام می‌شود.",
    ar: "بطاقة مصرفية أو عملات رقمية (TON و USDT) — تتم معالجة المدفوعات عبر مزوّدين معتمدين.",
    es: "Tarjeta de débito/crédito o cripto (TON, USDT): los pagos los procesan proveedores certificados.",
    ne: "डेबिट/क्रेडिट कार्ड वा क्रिप्टो (TON, USDT) — भुक्तानी प्रमाणित प्रदायकहरूमार्फत हुन्छ।",
    fr: "Carte bancaire ou crypto (TON, USDT) : les paiements sont traités par des prestataires certifiés.",
  },
  "how.flow.6": {
    en: "Token sent",
    ru: "Токен отправлен",
    fa: "توکن ارسال شد",
    ar: "تم إرسال الرمز",
    es: "Token enviado",
    ne: "टोकन पठाइयो",
    fr: "Jeton envoyé",
  },
  "how.flow.6.d": {
    en: "You receive a token by e-mail — use it to connect other devices or to re-connect your current one.",
    ru: "Токен придёт на e-mail — используйте его, чтобы подключить другие устройства или восстановить подключение на текущем.",
    fa: "توکن با ایمیل برای شما ارسال می‌شود — با آن دستگاه‌های دیگر را متصل کنید یا اتصال همین دستگاه را بازیابید.",
    ar: "يصلك الرمز عبر البريد الإلكتروني — استخدمه لربط أجهزة أخرى أو لإعادة اتصال جهازك الحالي.",
    es: "Recibes un token por correo electrónico — úsalo para conectar otros dispositivos o reconectar el actual.",
    ne: "टोकन इमेलमा आउँछ — अरू डिभाइसहरू जडान गर्न वा हालको डिभाइस पुनः जडान गर्न यसको प्रयोग गर्नुहोस्।",
    fr: "Vous recevez un jeton par e-mail — servez-vous-en pour connecter d’autres appareils ou reconnecter l’appareil actuel.",
  },
  "how.flow.7": {
    en: "Get More",
    ru: "Получите больше",
    fa: "بیشتر دریافت کنید",
    ar: "احصل على المزيد",
    es: "Obtén más",
    ne: "थप पाउनुहोस्",
    fr: "Allez plus loin",
  },
  "how.flow.7.d": {
    en: "Join our Telegram channel with your TG login, or get quick connect to your account — no app needed.",
    ru: "Вступайте в наш Telegram-канал по своему TG-логину или используйте быстрый вход в аккаунт — без приложения.",
    fa: "با لاگین تلگرام به کانال ما بپیوندید، یا بدون اپلیکیشن به حساب خود دسترسی سریع داشته باشید.",
    ar: "انضم إلى قناتنا على تيليجرام بحسابك في TG، أو استخدم الدخول السريع إلى حسابك دون التطبيق.",
    es: "Únete a nuestro canal de Telegram con tu usuario de TG, o accede rápido a tu cuenta sin la app.",
    ne: "आफ्नो TG लगइन प्रयोग गरेर हाम्रो टेलिग्राम च्यानलमा सामेल हुनुहोस्, वा एपविनै खातामा छिटो जडान लिनुहोस्।",
    fr: "Rejoignez notre canal Telegram avec votre identifiant TG, ou accédez rapidement à votre compte sans l’application.",
  },
  "how.flow.lead": {
    en: "Install, tap Connect, and you’re online in under a minute — then try it free for 3 days.",
    ru: "Установите приложение, нажмите «Подключить» — и вы онлайн меньше чем через минуту. Первые 3 дня — бесплатно.",
    fa: "نصب کنید، روی «اتصال» بزنید — و در کمتر از یک دقیقه آنلاین شوید. ۳ روز اول رایگان است.",
    ar: "ثبّت التطبيق واضغط «اتصال» — وستكون متصلاً في أقل من دقيقة. أول 3 أيام مجانية.",
    es: "Instala, toca «Conectar» y estarás en línea en menos de un minuto. Los primeros 3 días son gratis.",
    ne: "इन्स्टल गर्नुहोस्, «जडान» थिच्नुहोस् — एक मिनेटभित्रै अनलाइन हुनुहुन्छ। पहिलो ३ दिन निःशुल्क।",
    fr: "Installez, touchez « Se connecter » — vous êtes en ligne en moins d’une minute. Les 3 premiers jours sont gratuits.",
  },
  "how.flow.g1": {
    en: "Get connected",
    ru: "Подключение",
    fa: "متصل شوید",
    ar: "اتصل",
    es: "Conéctate",
    ne: "जडान गर्नुहोस्",
    fr: "Connectez-vous",
  },
  "how.flow.g2": {
    en: "Then keep going",
    ru: "Что дальше",
    fa: "و پس از آن",
    ar: "ثم تابع",
    es: "Y después",
    ne: "त्यसपछि",
    fr: "Et ensuite",
  },
  "price.h1a": {
    en: "Simple, honest",
    ru: "Простые, честные",
    fa: "ساده، صادقانه",
    ar: "أسعار بسيطة",
    es: "Precios simples",
    ne: "सरल, इमानदार",
    fr: "Des tarifs simples",
  },
  "price.h1b": {
    en: "pricing.",
    ru: "цены.",
    fa: "قیمت‌گذاری.",
    ar: "وصادقة.",
    es: "y honestos.",
    ne: "मूल्य निर्धारण।",
    fr: "et honnêtes.",
  },
  "price.sub": {
    en: "One plan. Everything included. Prices in USD — pay by debit/credit card or crypto (USDT / TON). No surprises.",
    ru: "Один тариф. Всё включено. Цены в рублях — оплата картой, СБП или криптой (USDT / TON). Без сюрпризов.",
    fa: "یک طرح. همه چیز شامل است. پرداخت با کارت بانکی یا رمزارز. بدون غافلگیری.",
    ar: "خطة واحدة. كل شيء مشمول. ادفع ببطاقة مصرفية أو عملات رقمية. بدون مفاجآت.",
    es: "Un plan. Todo incluido. Paga con tarjeta de débito/crédito o cripto. Sin sorpresas.",
    ne: "एउटा योजना। सबै कुरा समावेश। डेबिट/क्रेडिट कार्ड वा क्रिप्टोबारत भुक्तानी। कुनै आश्चर्य छैन।",
    fr: "Un forfait. Tout inclus. Payez par carte bancaire ou crypto. Sans surprises.",
  },
  "price.popular": {
    en: "Most Popular",
    ru: "Самый популярный",
    fa: "محبوب‌ترین",
    ar: "الأكثر شيوعًا",
    es: "El más popular",
    ne: "सबैभन्दा लोकप्रिय",
    fr: "Le plus populaire",
  },


  "price.refund.h": {
    en: "Refund policy",
    ru: "Политика возврата",
    fa: "سیاست بازگشت",
    ar: "سياسة الاسترداد",
    es: "Política de reembolso",
    ne: "फिर्ता नीति",
    fr: "Politique de remboursement",
  },
  "price.refund.p": {
    en: "If NullVPN does not work in your location within 48 hours of purchase, contact us on Telegram for a full refund. No questions asked.",
    ru: "Если NullVPN не работает в вашем месте в течение 48 часов после покупки, свяжитесь с нами в Telegram для полного возврата средств. Без вопросов.",
    fa: "اگر NullVPN در موقعیت شما در عرض ۴۸ ساعت پس از خرید کار نکرد، برای بازپرداخت کامل با ما در تلگرام تماس بگیرید. بدون سوال.",
    ar: "إذا لم يعمل NullVPN في موقعك خلال 48 ساعة من الشراء، راسلنا على تيليجرام لاسترداد كامل المبلغ. بدون أسئلة.",
    es: "Si NullVPN no funciona en tu ubicación dentro de las 48 horas posteriores a la compra, escríbenos por Telegram para un reembolso completo. Sin preguntas.",
    ne: "यदि खरिद गरेको ४८ घण्टाभित्र तपाईंको स्थानमा NullVPN काम गर्दैन भने, पूर्ण फिर्ताका लागि Telegram मा हामीलाई सम्पर्क गर्नुहोस्। कुनै प्रश्न सोधिँदैन।",
    fr: "Si NullVPN ne fonctionne pas chez vous dans les 48 heures suivant l'achat, écrivez-nous sur Telegram pour un remboursement complet. Sans questions.",
  },
  "faq.cat.group": {
    en: "Filter questions by topic",
    ru: "Фильтр вопросов по теме",
    fa: "فیلتر پرسش‌ها بر اساس موضوع",
    ar: "تصفية الأسئلة حسب الموضوع",
    es: "Filtrar preguntas por tema",
    ne: "विषय अनुसार प्रश्नहरू फिल्टर गर्नुहोस्",
    fr: "Filtrer les questions par sujet",
  },
  "faq.cat.all": {
    en: "All",
    ru: "Все",
    fa: "همه",
    ar: "الكل",
    es: "Todas",
    ne: "सबै",
    fr: "Toutes",
  },
  "faq.cat.privacy": {
    en: "Privacy",
    ru: "Приватность",
    fa: "حریم خصوصی",
    ar: "الخصوصية",
    es: "Privacidad",
    ne: "गोपनीयता",
    fr: "Confidentialité",
  },
  "faq.cat.pay": {
    en: "Payments",
    ru: "Оплата",
    fa: "پرداخت‌ها",
    ar: "المدفوعات",
    es: "Pagos",
    ne: "भुक्तानी",
    fr: "Paiements",
  },
  "faq.cat.devices": {
    en: "Devices",
    ru: "Устройства",
    fa: "دستگاه‌ها",
    ar: "الأجهزة",
    es: "Dispositivos",
    ne: "उपकरणहरू",
    fr: "Appareils",
  },
  "faq.cat.access": {
    en: "Access & features",
    ru: "Доступ и функции",
    fa: "دسترسی و قابلیت‌ها",
    ar: "الوصول والميزات",
    es: "Acceso y funciones",
    ne: "पहुँच र सुविधाहरू",
    fr: "Accès et fonctions",
  },
  "faq.q1": {
    en: "Do you keep logs?",
    ru: "Вы ведёте логи?",
    fa: "آیا NullVPN واقعاً خصوصی است؟",
    ar: "هل تحتفظون بسجلات؟",
    es: "¿Se guardan registros?",
    ne: "के NullVPN साँच्चै निजी छ?",
    fr: "Conservez-vous des journaux ?",
  },
  "faq.a1": {
    en: "No activity logs — ever. We don't record the sites you visit, transmitted content, DNS queries through the tunnel, or your real IP address, and our servers operate under a strict no-logs policy. We keep only minimal operational data needed to run your subscription.",
    ru: "Журналов активности нет — никогда. Мы не записываем посещаемые сайты, содержимое передач, DNS-запросы через туннель и ваш реальный IP; наши серверы работают строго без логов. Храним только минимум операционных данных для подписки.",
    fa: "بله. بدون ثبت فعالیت، زمان اتصال، آدرس IP، یا سایت‌های بازدید شده. برای ثبت‌نام به اطلاعات شخصی نیاز نیست. پرداخت‌ها با ارز دیجیتال است و به هویت شما مرتبط نیست.",
    ar: "بلا سجلات نشاط — أبدًا. لا نسجل المواقع التي تزورها ولا المحتوى المنقول ولا استعلامات DNS عبر النفق ولا عنوان IP الحقيقي، وتعمل خوادمنا وفق سياسة صارمة بعدم الاحتفاظ بالسجلات. نحتفظ فقط بأقل قدر من البيانات التشغيلية اللازمة لتشغيل اشتراكك.",
    es: "Sin registros de actividad — nunca. No registramos los sitios que visitas, el contenido transmitido, las consultas DNS a través del túnel ni tu dirección IP real, y nuestros servidores operan bajo una estricta política de no-logs. Solo conservamos los datos operativos mínimos necesarios para gestionar tu suscripción.",
    ne: "हो। गतिविधि, जडान समय, IP, वा भ्रमण गरिएका साइटहरूको कुनै लग छैन। साइन अप गर्न कुनै व्यक्तिगत जानकारी आवश्यक छैन। भुगतानहरू क्रिप्टोकरेन्सीमा छन्, तपाईंको पहिचानसँग जोडिएको छैन।",
    fr: "Aucun journal d'activité — jamais. Nous n'enregistrons ni les sites que vous visitez, ni le contenu transmis, ni les requêtes DNS traversant le tunnel, ni votre véritable adresse IP, et nos serveurs fonctionnent sous une stricte politique de non-journalisation. Nous ne conservons que les données opérationnelles minimales nécessaires à la gestion de votre abonnement.",
  },
  "faq.q2": {
    en: "Will it work on my network?",
    ru: "Будет ли работать в моей сети?",
    fa: "آیا در شبکه‌های محدود کار می‌کند؟",
    ar: "هل ستعمل على شبكتي؟",
    es: "¿Funcionará en mi red?",
    ne: "के यो प्रतिबन्धित सञ्जालहरूमा काम गर्छ?",
    fr: "Fonctionnera-t-il sur mon réseau ?",
  },
  "faq.a2": {
    en: "NullVPN is designed to work on mobile data, fixed broadband, and restrictive network environments. If you run into trouble, contact us on Telegram — we'll fix it or refund you.",
    ru: "NullVPN рассчитан на мобильный интернет, проводные сети и сложные сетевые окружения. Если что-то не так — напишите в Telegram: исправим или вернём деньги.",
    fa: "بله. به طور خاص برای محیط‌های محدود طراحی شده است. اگر با مشکلی مواجه شدید، با ما در تلگرام تماس بگیرید — ما آن را رفع می‌کنیم یا پول شما را برمی‌گردانیم.",
    ar: "صُمم NullVPN ليعمل على بيانات الجوال والخط الثابت وبيئات الشبكات المقيدة. إن واجهتك مشكلة، تواصل معنا على Telegram — نصلحها أو نسترد أموالك.",
    es: "NullVPN está diseñado para funcionar con datos móviles, banda ancha fija y entornos de red restrictivos. Si tienes problemas, escríbenos por Telegram — lo arreglamos o te reembolsamos.",
    ne: "हो। विशेष गरी प्रतिबन्धित वातावरणका लागि डिजाइन गरिएको। यदि तपाईंलाई समस्याहरू आउँछन् भने, Telegram मा हामीलाई सम्पर्क गर्नुहोस् — हामी यसलाई ठीक गर्नेछौं वा तपाईंलाई फिर्ता गर्नेछौं।",
    fr: "NullVPN est conçu pour fonctionner sur les données mobiles, la bande fixe et les environnements réseau restrictifs. En cas de souci, contactez-nous sur Telegram — nous corrigeons ou nous remboursons.",
  },
  "faq.q3": {
    en: "What devices are supported?",
    ru: "Какие устройства поддерживаются?",
    fa: "کدام دستگاه‌ها پشتیبانی می‌شوند؟",
    ar: "ما الأجهزة المدعومة؟",
    es: "¿Qué dispositivos son compatibles?",
    ne: "कुन उपकरणहरू समर्थित छन्?",
    fr: "Quels appareils sont pris en charge ?",
  },
  "faq.a3": {
    en: "Android phones and tablets via our dedicated app, routers running our custom firmware (protecting every device behind them), and other platforms via standard configuration files — full instructions provided after purchase.",
    ru: "Android-телефоны и планшеты через наше приложение, роутеры с нашей прошивкой (защищают все устройства за ними) и остальные платформы через стандартные конфигурации — инструкции после покупки.",
    fa: "گوشی‌ها و تبلت‌های اندرویدی از طریق اپ اختصاصی ما، روترهای دارای فریمور اختصاصی ما (محافظت از همه دستگاه‌های پشت آن) و سایر پلتفرم‌ها از طریق فایل‌های پیکربندی استاندارد — دستورالعمل‌های کامل پس از خرید ارائه می‌شود.",
    ar: "هواتف وأجهزة لوحية بأندرويد عبر تطبيقنا المخصص، وأجهزة راوتر تعمل بنظامنا المخصص (تحمي كل جهاز خلفها)، ومنصات أخرى عبر ملفات إعداد قياسية — الإرشادات الكاملة تُقدَّم بعد الشراء.",
    es: "Teléfonos y tabletas Android mediante nuestra aplicación dedicada, routers con nuestro firmware propio (protegiendo cada dispositivo detrás de ellos) y otras plataformas mediante archivos de configuración estándar — instrucciones completas tras la compra.",
    ne: "हाम्रो समर्पित एपमार्फत एन्ड्रोइड फोन र ट्याब्लेट, हाम्रो अनुकूलित फर्मवेयर चल्ने राउटरहरू (तिनीहरू पछाडिका सबै उपकरण सुरक्षित गर्दै), र अन्य प्लेटफर्महरू मानक कन्फिगरेसन फाइलमार्फत — खरिदपछि पूर्ण निर्देशन उपलब्ध हुन्छ।",
    fr: "Téléphones et tablettes Android via notre application dédiée, routeurs avec notre firmware personnalisé (protégeant chaque appareil derrière eux), et autres plateformes via des fichiers de configuration standard — instructions complètes fournies après l'achat.",
  },
  "faq.q4": {
    en: "How do I pay?",
    ru: "Как оплатить?",
    fa: "چطور پرداخت کنم؟",
    ar: "كيف أدفع؟",
    es: "¿Cómo pago?",
    ne: "म कसरी भुगतान गर्ने?",
    fr: "Comment payer ?",
  },
  "faq.a4": {
    en: "With debit/credit cards or crypto (TON, USDT and others). Payments are processed by certified third-party providers — we never see or store your full card details. Confirmed within seconds, connection delivered automatically.",
    ru: "Картой, через СБП или криптой (TON, USDT и др.). Платежи обрабатывают сертифицированные сторонние провайдеры — полные данные карты нам не видны. Подтверждение за секунды, подключение автоматически.",
    fa: "با ارز دیجیتال TON با استفاده از Tonkeeper، MyTonWallet یا هر کیف پول TON. در چند ثانیه تأیید می‌شود، اتصال به صورت خودکار تحویل داده می‌شود.",
    ar: "ببطاقات بنكية أو عملات رقمية (TON وUSDT وغيرها). تعالج المدفوعات عبر جهات خارجية معتمدة — لا نرى ولا نخزن بيانات بطاقتك الكاملة أبدًا. التأكيد خلال ثوانٍ ويُسلَّم الاتصال تلقائيًا.",
    es: "Con tarjetas de débito/crédito o cripto (TON, USDT y otras). Los pagos los procesan proveedores externos certificados — nunca vemos ni almacenamos los datos completos de tu tarjeta. Confirmado en segundos, la conexión se entrega automáticamente.",
    ne: "Tonkeeper, MyTonWallet, वा कुनै पनि TON वालेट प्रयोग गरेर TON क्रिप्टोकरेन्सीसँग। सेकेन्डमा पुष्टि, जडान स्वचालित रूपमा वितरित।",
    fr: "Par carte bancaire ou en crypto (TON, USDT et autres). Les paiements sont traités par des prestataires certifiés — nous ne voyons ni ne stockons jamais les données complètes de votre carte. Confirmé en quelques secondes, la connexion est livrée automatiquement.",
  },
  "faq.q5": {
    en: "Where else can I reach NullVPN?",
    ru: "Где ещё доступен NullVPN?",
    fa: "اگر nullvpn.net مسدود باشد چه؟",
    ar: "أين يمكنني الوصول إلى NullVPN؟",
    es: "¿Dónde más puedo contactar a NullVPN?",
    ne: "यदि nullvpn.net असफल भएमा के?",
    fr: "Par quels autres moyens joindre NullVPN ?",
  },
  "faq.a5": {
    en: "Our Telegram bot <a href=\"https://t.me/nullvpnnetbot\" target=\"_blank\" rel=\"noopener\" referrerpolicy=\"no-referrer\">@nullvpnnetbot</a> and our <a href=\"web3.html\" target=\"_blank\" rel=\"noopener\" referrerpolicy=\"no-referrer\">TON Web3 mirror page</a> — works in any browser.",
    ru: "Telegram-бот <a href=\"https://t.me/nullvpnnetbot\" target=\"_blank\" rel=\"noopener\" referrerpolicy=\"no-referrer\">@nullvpnnetbot</a> и наше <a href=\"web3.html\" target=\"_blank\" rel=\"noopener\" referrerpolicy=\"no-referrer\">Web3-зеркало на TON</a> — в любом браузере.",
    fa: "از <a href=\"https://t.me/nullvpnnet\" target=\"_blank\" rel=\"noopener\" referrerpolicy=\"no-referrer\">@nullvpnnet در تلگرام</a>، ربات <a href=\"https://t.me/nullvpnnetbot\" target=\"_blank\" rel=\"noopener\" referrerpolicy=\"no-referrer\">@nullvpnnetbot</a>، یا <a href=\"web3.html\" target=\"_blank\" rel=\"noopener\" referrerpolicy=\"no-referrer\">صفحهٔ TON Web3</a> استفاده کنید — در هر مرورگر کار می‌کند.",
    ar: "بوت Telegram <a href=\"https://t.me/nullvpnnetbot\" target=\"_blank\" rel=\"noopener\" referrerpolicy=\"no-referrer\">@nullvpnnetbot</a> وصفحتنا المرآة على <a href=\"web3.html\" target=\"_blank\" rel=\"noopener\" referrerpolicy=\"no-referrer\">TON Web3</a> — تعمل في أي متصفح.",
    es: "Nuestro bot de Telegram <a href=\\\"https://t.me/nullvpnnetbot\\\" target=\\\"_blank\\\" rel=\\\"noopener\\\" referrerpolicy=\\\"no-referrer\\\">@nullvpnnetbot</a> y nuestra <a href=\\\"web3.html\\\" target=\\\"_blank\\\" rel=\\\"noopener\\\" referrerpolicy=\\\"no-referrer\\\">página espejo TON Web3</a> — funcionan en cualquier navegador.",
    ne: "Telegram मा <a href=\"https://t.me/nullvpnnet\" target=\"_blank\" rel=\"noopener\" referrerpolicy=\"no-referrer\">@nullvpnnet</a>, बट <a href=\"https://t.me/nullvpnnetbot\" target=\"_blank\" rel=\"noopener\" referrerpolicy=\"no-referrer\">@nullvpnnetbot</a>, वा <a href=\"web3.html\" target=\"_blank\" rel=\"noopener\" referrerpolicy=\"no-referrer\">हाम्रो TON Web3 पृष्ठ</a> प्रयोग गर्नुहोस् — कुनै पनि ब्राउजरमा काम गर्छ।",
    fr: "Notre bot Telegram <a href=\\\"https://t.me/nullvpnnetbot\\\" target=\\\"_blank\\\" rel=\\\"noopener\\\" referrerpolicy=\\\"no-referrer\\\">@nullvpnnetbot</a> et notre <a href=\\\"web3.html\\\" target=\\\"_blank\\\" rel=\\\"noopener\\\" referrerpolicy=\\\"no-referrer\\\">page miroir TON Web3</a> — fonctionnent dans n'importe quel navigateur.",
  },
  "faq.q6": {
    en: "Can I get a refund?",
    ru: "Можно получить возврат?",
    fa: "آیا می‌توانم بازگشت وجه دریافت کنم؟",
    ar: "هل يمكنني استرداد المبلغ؟",
    es: "¿Puedo obtener un reembolso?",
    ne: "के म फिर्ता पाउन सक्छु?",
    fr: "Puis-je être remboursé ?",
  },
  "faq.a6": {
    en: "Yes. If it doesn't work within 48 hours, message us on Telegram for a full refund. No questions asked.",
    ru: "Да. Если не работает в течение 48 часов, напишите нам в Telegram для полного возврата. Без вопросов.",
    fa: "بله. اگر در عرض ۴۸ ساعت کار نکرد، برای بازپرداخت کامل در تلگرام به ما پیام بدهید. بدون سوال.",
    ar: "نعم. إذا لم يكن يعمل خلال 48 ساعة، راسلنا على تيليجرام لاسترداد كامل المبلغ. بدون أسئلة.",
    es: "Sí. Si no funciona dentro de las 48 horas, escríbenos por Telegram para un reembolso completo. Sin preguntas.",
    ne: "हो। यदि ४८ घण्टाभित्र काम गर्दैन भने, पूर्ण फिर्ताका लागि Telegram मा हामीलाई सन्देश पठाउनुहोस्। कुनै प्रश्न सोधिँदैन।",
    fr: "Oui. Si ça ne fonctionne pas dans les 48 heures, écrivez-nous sur Telegram pour un remboursement complet. Sans questions.",
  },
  "faq.q7": {
    en: "How many devices can I use?",
    ru: "Сколько устройств можно использовать?",
    fa: "چند دستگاه می‌توانم استفاده کنم؟",
    ar: "كم جهازًا يمكنني استخدام؟",
    es: "¿Cuántos dispositivos puedo usar?",
    ne: "म कति उपकरणहरू प्रयोग गर्न सक्छु?",
    fr: "Combien d'appareils puis-je utiliser ?",
  },
  "faq.a7": {
    en: "Up to 10 devices on one subscription. For team or family setups, message us on Telegram.",
    ru: "До 10 устройств на одну подписку. Для команды или семьи напишите нам в Telegram.",
    fa: "تا ۱۰ دستگاه با یک اشتراک. برای تنظیمات تیمی یا خانوادگی در تلگرام به ما پیام بدهید.",
    ar: "حتى ١٠ أجهزة لكل اشتراك. لإعدادات الفريق أو العائلة، راسلنا على تيليجرام.",
    es: "Hasta 10 dispositivos por suscripción. Para uso en equipo o familia, escríbenos por Telegram.",
    ne: "एक सदस्यतामा १० सम्म उपकरणहरू। टोली वा परिवारका सेटअपका लागि हामीलाई Telegram मा सन्देश पठाउनुहोस्।",
    fr: "Jusqu'à 10 appareils par abonnement. Pour un usage en équipe ou en famille, écrivez-nous sur Telegram.",
  },
  "faq.q8": {
    en: "Is NullVPN legal?",
    ru: "NullVPN законен?",
    fa: "آیا NullVPN قانونی است؟",
    ar: "هل استخدام NullVPN قانوني؟",
    es: "¿Es legal NullVPN?",
    ne: "के NullVPN कानूनी छ?",
    fr: "NullVPN est-il légal ?",
  },
  "faq.a8": {
    en: "Private connectivity tools are legal in most countries. Please check your local laws. NullVPN does not condone illegal activity.",
    ru: "Средства приватного соединения легальны в большинстве стран. Проверьте местное законодательство. NullVPN не поддерживает незаконную деятельность.",
    fa: "استفاده از VPN در اکثر کشورها قانونی است. لطفاً قوانین محلی خود را بررسی کنید. NullVPN فعالیت غیرقانونی را تأیید نمی‌کند.",
    ar: "أدوات الاتصال الخاص قانونية في معظم الدول. يرجى الاطلاع على قوانين بلدك. لا يتغاضى NullVPN عن أي نشاط غير قانوني.",
    es: "Las herramientas de conectividad privada son legales en la mayoría de los países. Consulta tus leyes locales. NullVPN no tolera actividades ilegales.",
    ne: "अधिकांश देशहरूमा VPN प्रयोग गर्नु कानूनी छ। कृपया आफ्नो स्थानीय कानूनहरू जाँच गर्नुहोस्। NullVPN अवैध गतिविधिलाई अनुमोदन गर्दैन।",
    fr: "Les outils de connectivité privée sont légaux dans la plupart des pays. Vérifiez vos lois locales. NullVPN ne tolère aucune activité illégale.",
  },
  "faq.q9": {
    en: "Can I share my connection with someone else?",
    ru: "Можно ли поделиться соединением?",
    fa: "می‌توانم اتصالم را با دیگری به اشتراک بگذارم؟",
    ar: "هل يمكنني مشاركة اتصالي مع شخص آخر؟",
    es: "¿Puedo compartir mi conexión con otra persona?",
    ne: "के म आफ्नो जडान अरूसँग सेयर गर्न सक्छु?",
    fr: "Puis-je partager ma connexion avec quelqu'un d'autre ?",
  },
  "faq.a9": {
    en: "Your tunnel is personal and tied to your subscription. Need coverage for family or a team? Message us on Telegram — we'll arrange extra devices.",
    ru: "Туннель персональный и привязан к подписке. Нужно покрытие для семьи или команды? Напишите в Telegram — добавим устройства.",
    fa: "تونل شما شخصی است و به اشتراک شما گره خورده است. برای پوشش خانواده یا تیم به ما در تلگرام پیام دهید — دستگاه‌های اضافی را فراهم می‌کنیم.",
    ar: "نفقك شخصي ومرتبط باشتراكك. تحتاج تغطية لعائلتك أو فريقك؟ راسلنا على Telegram — سنرتب أجهزة إضافية.",
    es: "Tu túnel es personal y está vinculado a tu suscripción. ¿Necesitas cobertura para tu familia o equipo? Escríbenos por Telegram y organizamos dispositivos adicionales.",
    ne: "तपाईंको टनेल व्यक्तिगत छ र तपाईंको सदस्यतासँग जोडिएको छ। परिवार वा टिमका लागि कभरेज चाहिन्छ? टेलिग्राममा हामीलाई सन्देश पठाउनुहोस् — हामी थप उपकरणहरू मिलाउँछौं।",
    fr: "Votre tunnel est personnel et lié à votre abonnement. Besoin d'une couverture pour votre famille ou votre équipe ? Écrivez-nous sur Telegram et nous ajouterons des appareils supplémentaires.",
  },
  "faq.cta.h": {
    en: "Still have questions?",
    ru: "Остались вопросы?",
    fa: "هنوز سوال دارید؟",
    ar: "لا تزال لديك أسئلة؟",
    es: "¿Sigues con dudas?",
    ne: "अझै प्रश्नहरू छन्?",
    fr: "Encore des questions ?",
  },
  "faq.cta.p": {
    en: "Message us on Telegram — we reply fast.",
    ru: "Напишите нам в Telegram — мы отвечаем быстро.",
    fa: "در تلگرام به ما پیام بدهید — ما سریع پاسخ می‌دهیم.",
    ar: "راسلنا على Telegram — نرد بسرعة.",
    es: "Escríbenos por Telegram — respondemos rápido.",
    ne: "Telegram मा हामीलाई सन्देश पठाउनुहोस् — हामी छिटो जवाफ दिन्छौं।",
    fr: "Écrivez-nous sur Telegram — nous répondons vite.",
  },
  "faq.cta.btn": {
    en: "Contact on Telegram →",
    ru: "Написать в Telegram →",
    fa: "تماس در تلگرام →",
    ar: "تواصل عبر Telegram →",
    es: "Contactar por Telegram →",
    ne: "Telegram मा सम्पर्क गर्नुहोस् →",
    fr: "Contacter sur Telegram →",
  },









  "contact.h1": {
    en: "Get in touch",
    ru: "Свяжитесь с нами",
    fa: "تماس بگیرید",
    ar: "تواصل معنا",
    es: "Contáctanos",
    ne: "सम्पर्क गर्नुहोस्",
    fr: "Nous contacter",
  },
  "contact.sub": {
    en: "Support on Telegram (<a href=\"https://t.me/nullvpn_net\" target=\"_blank\" rel=\"noopener\" referrerpolicy=\"no-referrer\">@nullvpn_net</a>) or <a href=\"mailto:support@nullvpn.net\">support@nullvpn.net</a>. We respond fast.",
    ru: "Поддержка в Telegram (<a href=\"https://t.me/nullvpn_net\" target=\"_blank\" rel=\"noopener\" referrerpolicy=\"no-referrer\">@nullvpn_net</a>) или на <a href=\"mailto:support@nullvpn.net\">support@nullvpn.net</a>. Отвечаем быстро.",
    fa: "پشتیبانی در تلگرام (<a href=\"https://t.me/nullvpn_net\" target=\"_blank\" rel=\"noopener\" referrerpolicy=\"no-referrer\">@nullvpn_net</a>) یا <a href=\"mailto:support@nullvpn.net\">support@nullvpn.net</a>. سریع پاسخ می‌دهیم.",
    ar: "الدعم عبر تلجرام (<a href=\"https://t.me/nullvpn_net\" target=\"_blank\" rel=\"noopener\" referrerpolicy=\"no-referrer\">@nullvpn_net</a>) أو <a href=\"mailto:support@nullvpn.net\">support@nullvpn.net</a>. نرد بسرعة.",
    es: "Soporte en Telegram (<a href=\"https://t.me/nullvpn_net\" target=\"_blank\" rel=\"noopener\" referrerpolicy=\"no-referrer\">@nullvpn_net</a>) o en <a href=\"mailto:support@nullvpn.net\">support@nullvpn.net</a>. Respondemos rápido.",
    ne: "Telegram मा समर्थन (<a href=\"https://t.me/nullvpn_net\" target=\"_blank\" rel=\"noopener\" referrerpolicy=\"no-referrer\">@nullvpn_net</a>) वा <a href=\"mailto:support@nullvpn.net\">support@nullvpn.net</a>। हामी छिटो प्रतिक्रिया दिन्छौँ।",
    fr: "Assistance sur Telegram (<a href=\"https://t.me/nullvpn_net\" target=\"_blank\" rel=\"noopener\" referrerpolicy=\"no-referrer\">@nullvpn_net</a>) ou par e-mail <a href=\"mailto:support@nullvpn.net\">support@nullvpn.net</a>. Nous répondons vite.",
  },
  "contact.bot.h": {
    en: "Telegram Bot",
    ru: "Telegram Бот",
    fa: "ربات تلگرام",
    ar: "بوت تليجرام",
    es: "Bot de Telegram",
    ne: "Telegram बट",
    fr: "Bot Telegram",
  },
  "contact.bot.p": {
    en: "Backup purchase channel — buy or renew a plan, or ask for help. Automated and instant.",
    ru: "Резервный канал покупки — купить или продлить тариф, обратиться за помощью. Автоматически и мгновенно.",
    fa: "کانال خرید جایگزین — خرید یا تمدید طرح، یا دریافت کمک. خودکار و فوری.",
    ar: "قناة شراء احتياطية — اشترِ الخطة أو جدّدها أو اطلب المساعدة. تلقائي وفوري.",
    es: "Canal de compra alternativo — compra o renueva un plan, o pide ayuda. Automático e instantáneo.",
    ne: "बैकअप खरिद माध्यम — योजना किन्न वा नवीकरण गर्न, वा सहायता माग्न। स्वचालित र तुरुन्तै।",
    fr: "Canal d’achat de secours — achetez ou renouvelez un forfait, ou demandez de l’aide. Automatique et instantané.",
  },
  "contact.bot.btn": {
    en: "Open Bot →",
    ru: "Открыть бота →",
    fa: "باز کردن ربات →",
    ar: "افتح البوت →",
    es: "Abrir Bot →",
    ne: "बट खोल्नुहोस् →",
    fr: "Ouvrir le bot →",
  },
  "contact.ch.h": {
    en: "Telegram Channel",
    ru: "Telegram Канал",
    fa: "کانال تلگرام",
    ar: "قناة تليجرام",
    es: "Canal de Telegram",
    ne: "Telegram च्यानल",
    fr: "Canal Telegram",
  },
  "contact.ch.p": {
    en: "News, updates, server status, and announcements. Subscribe to stay informed.",
    ru: "Новости, обновления, статус сервера и объявления. Подпишитесь, чтобы быть в курсе.",
    fa: "اخبار، به‌روزرسانی‌ها، وضعیت سرور و اطلاعیه‌ها. برای مطلع ماندن مشترک شوید.",
    ar: "أخبار وتحديثات وحالة الخادم والإعلانات. اشترك لتبقى على اطلاع.",
    es: "Noticias, actualizaciones, estado del servidor y anuncios. Suscríbete para mantenerte informado.",
    ne: "समाचार, अपडेटहरू, सर्भर स्थिति र घोषणाहरू। सूचित रहन सदस्यता लिनुहोस्।",
    fr: "Actualités, mises à jour, état des serveurs et annonces. Abonnez-vous pour rester informé.",
  },
  "contact.ch.btn": {
    en: "Subscribe →",
    ru: "Подписаться →",
    fa: "مشترک شدن →",
    ar: "اشتراك →",
    es: "Suscribirse →",
    ne: "सदस्यता लिनुहोस् →",
    fr: "S'abonner →",
  },
  "contact.web3.h": {
    en: "TON Web3",
    ru: "TON Web3",
    fa: "TON Web3",
    ar: "TON Web3",
    es: "TON Web3",
    ne: "TON Web3",
    fr: "TON Web3",
  },
  "contact.web3.p": {
    en: "Access NullVPN through the TON Network — a mirror of this site, works in any browser.",
    ru: "Зеркало сайта в сети TON — открывается в любом браузере.",
    fa: "قابل دسترسی از طریق شبکه TON — حتی اگر این وبسایت مسدود باشد کار می‌کند. نیازی به VPN نیست.",
    ar: "يمكن الوصول إليه عبر شبكة TON — يعمل حتى لو كان هذا الموقع محظورًا. لا حاجة لـ VPN.",
    es: "Accesible a través de la Red TON — funciona incluso si este sitio web está bloqueado. No se necesita VPN.",
    ne: "TON नेटवर्क मार्फत पहुँचयोग्य — यो वेबसाइट असफल भए पनि काम गर्छ। VPN आवश्यक छैन।",
    fr: "Accédez à NullVPN via le réseau TON — un miroir de ce site, qui fonctionne dans n'importe quel navigateur.",
  },
  "contact.web3.btn": {
    en: "Open Web3 Site →",
    ru: "Открыть Web3 сайт →",
    fa: "باز کردن سایت Web3 →",
    ar: "افتح موقع Web3 →",
    es: "Abrir Sitio Web3 →",
    ne: "Web3 साइट खोल्नुहोस् →",
    fr: "Ouvrir le site Web3 →",
  },
  "contact.dl.h": {
    en: "Download App",
    ru: "Скачать приложение",
    fa: "دانلود برنامه",
    ar: "تنزيل التطبيق",
    es: "Descargar Aplicación",
    ne: "एप डाउनलोड गर्नुहोस्",
    fr: "Télécharger l'app",
  },
  "contact.dl.p": {
    en: "Get the Android APK directly — no app store needed. Works anywhere.",
    ru: "Получите Android APK напрямую — магазин приложений не нужен. Работает везде.",
    fa: "APK اندروید را مستقیماً دریافت کنید — نیازی به فروشگاه اپ نیست. همه جا کار می‌کند.",
    ar: "احصل على APK لنظام Android مباشرةً — لا حاجة لمتجر التطبيقات. يعمل في أي مكان.",
    es: "Obtén el APK de Android directamente — no se necesita tienda de aplicaciones. Funciona en cualquier lugar.",
    ne: "Android APK सिधै प्राप्त गर्नुहोस् — ऐप स्टोर आवश्यक छैन। कहीं पनि काम गर्छ।",
    fr: "Obtenez l'APK Android directement — sans magasin d'applications. Fonctionne partout.",
  },
  "contact.cta.h": {
    en: "Ready to connect?",
    ru: "Готовы подключиться?",
    fa: "آماده اتصال هستید؟",
    ar: "مستعد للاتصال؟",
    es: "¿Listo para conectarte?",
    ne: "जडान गर्न तयार हुनुहुन्छ?",
    fr: "Prêt à vous connecter ?",
  },
  "contact.cta.p": {
    en: "From $3/month. No account. Works in 60 seconds.",
    ru: "От 300 ₽/мес. Без аккаунта. Работает за 60 секунд.",
    fa: "از ۳ دلار/ماه. بدون حساب. در ۶۰ ثانیه کار می‌کند.",
    ar: "ابتداءً من 3 دولارات/شهر. بدون حساب. يعمل في 60 ثانية.",
    es: "Desde $3/mes. Sin cuenta. Funciona en 60 segundos.",
    ne: "$3/महिनाबाट। कुनै खाता छैन। ६० सेकेन्डमा काम गर्छ।",
    fr: "Dès $3/mois. Sans compte. En 60 secondes.",
  },
  "contact.cta.btn": {
    en: "See Pricing →",
    ru: "Смотреть цены →",
    fa: "مشاهده قیمت‌ها →",
    ar: "اطّلع على الأسعار →",
    es: "Ver precios →",
    ne: "मूल्य हेर्नुहोस् →",
    fr: "Voir les tarifs →",
  },
  "priv.h1a": {
    en: "Privacy",
    ru: "Политика",
    fa: "سیاست",
    ar: "سياسة",
    es: "Política de",
    ne: "गोपनीयता",
    fr: "Politique de",
  },
  "priv.h1b": {
    en: "Policy",
    ru: "конфиденциальности",
    fa: "حریم خصوصی",
    ar: "الخصوصية",
    es: "Privacidad",
    ne: "नीति",
    fr: "confidentialité",
  },
  "priv.updated": {
    en: "Last updated: March 2026",
    ru: "Последнее обновление: март 2026",
    fa: "آخرین به‌روزرسانی: مارس ۲۰۲۶",
    ar: "آخر تحديث: مارس 2026",
    es: "Última actualización: marzo de 2026",
    ne: "अन्तिम अपडेट: मार्च २०२६",
    fr: "Dernière mise à jour : mars 2026",
  },
  "legal.toc": {
    en: "On this page",
    ru: "На этой странице",
    fa: "در این صفحه",
    ar: "في هذه الصفحة",
    es: "En esta página",
    ne: "यो पृष्ठमा",
    fr: "Sur cette page",
  },
  "priv.q1": {
    en: "What data do we collect?",
    ru: "Какие данные мы собираем?",
    fa: "چه داده‌هایی جمع‌آوری می‌کنیم؟",
    ar: "ما البيانات التي نجمعها؟",
    es: "¿Qué datos recopilamos?",
    ne: "हामी कुन डेटा सङ्कलन गर्छौं?",
    fr: "Quelles données collectons-nous ?",
  },
  "priv.a1": {
    en: "Minimal by design. Sign-in uses private access tokens — no passwords, and an email is optional (only if you want recovery links). We never collect names, phone numbers, device identifiers, or browsing data. Debit/credit card payments are processed directly by our certified payment partners; your full card number never reaches our servers.",
    ru: "Минимум по дизайну. Вход использует приватные токены доступа — без паролей; email необязателен (только если хотите ссылки для восстановления). Мы не собираем имена, номера телефонов, идентификаторы устройств или данные о браузинге. Платежи картами и СБП обрабатывают наши сертифицированные платёжные партнёры; полные данные карты никогда не попадают на наши серверы.",
    fa: "به‌طور طراحی حداقلی. ورود با توکن‌های دسترسی خصوصی انجام می‌شود — بدون رمز عبور، و ایمیل اختیاری است (فقط اگر لینک‌های بازیابی می‌خواهید). ما نام، شماره تلفن، شناسه‌های دستگاه یا داده مرور را جمع‌آوری نمی‌کنیم. پرداخت‌های کارت بانکی مستقیماً توسط شرکای پرداخت معتبر ما پردازش می‌شود؛ شماره کامل کارت هرگز به سرورهای ما نمی‌رسد.",
    ar: "الحد الأدنى بالتصميم. تسجيل الدخول يستخدم رموز وصول خاصة — بدون كلمات مرور، والبريد الإلكتروني اختياري (فقط إذا أردت روابط الاستعادة). لا نجمع أبدًا الأسماء أو أرقام الهواتف أو معرّفات الأجهزة أو بيانات التصفح. تتم معالجة مدفوعات البطاقات المصرفية مباشرة عبر شركاء الدفع المعتمدين لدينا؛ رقم بطاقتك الكامل لا يصل أبدًا إلى خوادمنا.",
    es: "Mínimos por diseño. El inicio de sesión usa tokens de acceso privados — sin contraseñas, y el correo electrónico es opcional (solo si quieres enlaces de recuperación). Nunca recopilamos nombres, números de teléfono, identificadores de dispositivo ni datos de navegación. Los pagos con tarjeta de débito/crédito los procesan directamente nuestros socios de pago certificados; tu número de tarjeta completo nunca llega a nuestros servidores.",
    ne: "डिजाइनअनुसार न्यूनतम। साइन इन निजी एक्सेस टोकनहरू प्रयोग गर्छ — पासवर्ड बिना, र इमेल ऐच्छिक छ (पुनःप्राप्ति लिंकहरू चाहेमा मात्र)। हामी नाम, फोन नम्बर, उपकरण पहिचानकर्ता वा ब्राउजिङ डाटा कहिल्यै सङ्कलन गर्दैनौं। डेबिट/क्रेडिट कार्ड भुक्तानी हाम्रा प्रमाणित भुक्तानी साझेदारहरूले सिधै प्रशोधन गर्छन्; तपाईंको पूर्ण कार्ड नम्बर हाम्रो सर्भरमा कहिल्यै पुग्दैन।",
    fr: "Minimal par conception. La connexion utilise des jetons d\'accès privés — sans mot de passe, et l\'e-mail est facultatif (uniquement si vous souhaitez des liens de récupération). Nous ne collectons jamais de noms, de numéros de téléphone, d\'identifiants d\'appareil ni de données de navigation. Les paiements par carte bancaire sont traités directement par nos partenaires de paiement certifiés ; le numéro complet de votre carte n\'atteint jamais nos serveurs.",
  },
  "priv.q2": {
    en: "Do we log your internet activity?",
    ru: "Регистрируем ли мы вашу интернет-активность?",
    fa: "آیا فعالیت اینترنتی شما را ثبت می‌کنیم؟",
    ar: "هل نسجل نشاطك على الإنترنت؟",
    es: "¿Registramos su actividad en internet?",
    ne: "के हामी तपाईंको इन्टरनेट गतिविधि लग गर्छौं?",
    fr: "Journalisons-nous votre activité internet ?",
  },
  "priv.a2": {
    en: "No. We keep no activity logs: we never record websites visited, transmitted content, DNS queries through the tunnel, or your real IP address. Our servers operate under a strict no-logs policy. We store no connection history in logs — neither on our side nor on yours. If you use the browser as your client, we recommend private tabs and similar tools so nothing is saved on your device.",
    ru: "Нет. Мы не ведём журналов активности: мы никогда не записываем посещённые сайты, передаваемое содержимое, DNS-запросы через туннель или ваш реальный IP-адрес. Наши серверы работают по строгой политике отсутствия логов. История соединений хранится только на вашем устройстве и никогда не загружается на серверы.",
    fa: "خیر. ما هیچ لاگ فعالیتی نگه نمی‌داریم: هرگز سایت‌های بازدید شده، محتوای ارسالی، درخواست‌های DNS از طریق تونل یا IP واقعی شما را ثبت نمی‌کنیم. سرورهای ما تحت سیاست سخت‌گیرانه عدم ثبت فعالیت کار می‌کنند. تاریخچه اتصال فقط روی دستگاه خودتان ذخیره می‌شود و هرگز آپلود نمی‌شود.",
    ar: "لا. لا نحتفظ بأي سجلات نشاط: لا نسجل أبدًا المواقع التي تزورها أو المحتوى المرسل أو استعلامات DNS عبر النفق أو عنوان IP الحقيقي الخاص بك. تعمل خوادمنا وفق سياسة صارمة بعدم الاحتفاظ بالسجلات. لا نخزّن أي سجل اتصالات — لا من جهتنا ولا من جهتك. إذا كنت تستخدم المتصفح كعميل، ننصح بالتبويبات الخاصة وأدوات مشابهة حتى لا يُحفظ شيء على جهازك.",
    es: "No. No conservamos registros de actividad: nunca registramos sitios visitados, contenido transmitido, consultas DNS a través del túnel ni tu dirección IP real. Nuestros servidores operan bajo una estricta política de no-registros. El historial de conexiones se guarda solo en tu dispositivo y nunca se sube.",
    ne: "होइन। हामी गतिविधि लग राख्दैनौं: हामीले भ्रमण गरिएका साइट, प्रेषित सामग्री, टनेलमार्फत DNS अनुरोध वा तपाईंको वास्तविक IP कहिल्यै रेकर्ड गर्दैनौं। हाम्रा सर्भरहरू कडा लग-निराकरण नीतिअन्तर्गत सञ्चालन हुन्छन्। जडान इतिहास केवल तपाईंको यन्त्रमा भण्डारण हुन्छ र कहिल्यै अपलोड हुँदैन।",
    fr: "Non. Nous ne gardons aucun journal d\'activité : nous n\'enregistrons jamais les sites visités, le contenu transmis, les requêtes DNS via le tunnel ni votre adresse IP réelle. Nos serveurs fonctionnent selon une stricte politique de zéro log. Aucun historique de connexion n\'est conservé — ni de notre côté ni du vôtre. Si vous utilisez le navigateur comme client, nous recommandons les onglets privés et outils similaires pour ne rien laisser sur votre appareil.",
  },
  "priv.q3": {
    en: "Do we share data with third parties?",
    ru: "Передаём ли мы данные третьим лицам?",
    fa: "آیا داده‌ها را با اشخاص ثالث به اشتراک می‌گذاریم؟",
    ar: "هل نشارك البيانات مع أطراف ثالثة؟",
    es: "¿Compartimos datos con terceros?",
    ne: "के हामी तेस्रो पक्षहरूसँग डेटा साझा गर्छौं?",
    fr: "Partageons-nous des données avec des tiers ?",
  },
  "priv.a3": {
    en: "We never sell or hand over your data to advertising networks or data brokers. The only third parties involved in the service are our hosting providers (who run servers under a no-logs policy and never see tunnel contents) and our certified payment partners (who process payments directly — we receive only a confirmation, not your card details).",
    ru: "Мы никогда не продаём и не передаём ваши данные рекламным сетям или брокерам данных. Единственные третьи стороны в сервисе — хостинг-провайдеры (эксплуатируют серверы по политике отсутствия логов и не видят содержимое туннеля) и наши сертифицированные платёжные партнёры (обрабатывают платежи напрямую — мы получаем только подтверждение, а не данные вашей карты).",
    fa: "هرگز داده‌های شما را به شبکه‌های تبلیغاتی یا کارگزاران داده نمی‌فروشیم یا واگذار نمی‌کنیم. تنها اشخاص ثالث درگیر در سرویس، ارائه‌دهندگان هاستینگ ما هستند (که سرورها را تحت سیاست عدم ثبت لاگ اداره می‌کنند و هرگز محتوای تونل را نمی‌بینند) و شرکای پرداخت مورد تأیید ما (که پرداخت‌ها را مستقیماً پردازش می‌کنند — ما فقط یک تأییدیه دریافت می‌کنیم، نه جزئیات کارت شما).",
    ar: "لا نبيع بياناتك أبدًا ولا نسلّمها لشبكات الإعلانات أو وسطاء البيانات. الأطراف الثالثة الوحيدة في الخدمة هم مزودو الاستضافة لدينا (يديرون الخوادم وفق سياسة عدم الاحتفاظ بالسجلات ولا يرون أبدًا محتوى النفق) وشركاء الدفع المعتمدون (يعالجون المدفوعات مباشرة — نستلم تأكيدًا فقط، وليس تفاصيل بطاقتك).",
    es: "Nunca vendemos ni entregamos tus datos a redes publicitarias o corredores de datos. Los únicos terceros involucrados en el servicio son nuestros proveedores de hosting (que operan servidores bajo una política de no-registros y nunca ven el contenido del túnel) y nuestros socios de pago certificados (que procesan los pagos directamente — solo recibimos una confirmación, no los datos de tu tarjeta).",
    ne: "हामी तपाईंको डाटा विज्ञापन नेटवर्क वा डाटा ब्रोकरलाई कहिल्यै बेच्दैनौं वा हस्तान्तरण गर्दैनौं। सेवामा संलग्न एकमात्र तेस्रो पक्षहरू हाम्रा होस्टिङ प्रदायकहरू हुन् (जसले लग-निराकरण नीतिअन्तर्गत सर्भर चलाउँछन् र टनेलको सामग्री कहिल्यै देख्दैनन्) र हाम्रा प्रमाणित भुगतान साझेदारहरू (जसले भुगतान सिधै प्रशोधन गर्छन् — हामी केवल पुष्टि प्राप्त गर्छौं, तपाईंको कार्ड विवरण होइन)।",
    fr: "Nous ne vendons ni ne transmettons vos données à des réseaux publicitaires ou des courtiers en données. Les seuls tiers impliqués sont nos hébergeurs (qui gèrent des serveurs sans logs et ne voient jamais le contenu du tunnel) et nos partenaires de paiement certifiés (qui traitent les paiements directement — nous ne recevons qu\'une confirmation, pas les détails de votre carte).",
  },
  "priv.q4": {
    en: "Cookies and analytics",
    ru: "Куки и аналитика",
    fa: "کوکی‌ها و تجزیه و تحلیل",
    ar: "ملفات تعريف الارتباط والتحليلات",
    es: "Cookies y analítica",
    ne: "कुकीज र विश्लेषण",
    fr: "Cookies et analytique",
  },
  "priv.a4": {
    en: "No third-party analytics trackers. No advertising cookies placed on your device.",
    ru: "Никаких сторонних аналитических трекеров. Никаких рекламных куки на вашем устройстве.",
    fa: "بدون ردیاب‌های تحلیلی شخص ثالث. بدون کوکی‌های تبلیغاتی روی دستگاه شما.",
    ar: "لا متتبعات تحليلات من أطراف ثالثة. لا ملفات تعريف ارتباط إعلانية على جهازك.",
    es: "Sin rastreadores de analítica de terceros. Sin cookies publicitarias en su dispositivo.",
    ne: "कुनै तेस्रो पक्ष विश्लेषण ट्र्याकर छैन। तपाईंको उपकरणमा कुनै विज्ञापन कुकी राखिँदैन।",
    fr: "Aucun traceur d\'analytique tiers. Aucun cookie publicitaire déposé sur votre appareil.",
  },
  "priv.q5": {
    en: "Passwordless sign-in",
    ru: "Вход без пароля",
    fa: "ورود بدون رمز عبور",
    ar: "تسجيل الدخول بدون كلمة مرور",
    es: "Inicio de sesión sin contraseña",
    ne: "पासवर्डबिना साइन इन",
    fr: "Connexion sans mot de passe",
  },
  "priv.a5": {
    en: "NullVPN uses passwordless authentication — there are no passwords to steal, leak, or reuse across services. Your device receives a private access token; email delivery is optional and used only to help you recover your token.",
    ru: "NullVPN использует вход без пароля — нет паролей, которые можно украсть, утечь или переиспользовать в других сервисах. Ваше устройство получает приватный токен доступа; ссылка из письма лишь подтверждает, что входитесь именно вы.",
    fa: "NullVPN از احراز هویت بدون رمز عبور استفاده می‌کند — هیچ رمزی وجود ندارد که قابل سرقت، افشا یا استفاده مجدد در سرویس‌های دیگر باشد. دستگاه شما یک توکن دسترسی خصوصی دریافت می‌کند؛ لینک ایمیلی صرفاً تأیید می‌کند که واقعاً خودتان در حال ورود هستید.",
    ar: "يستخدم NullVPN مصادقة بدون كلمة مرور — لا توجد كلمات مرور لسرقتها أو تسريبها أو إعادة استخدامها. يتلقى جهازك رمز وصول خاصًا؛ وإرسال البريد الإلكتروني اختياري ويُستخدم فقط لمساعدتك في استعادة الرمز.",
    es: "NullVPN usa autenticación sin contraseña — no hay contraseñas que robar, filtrar o reutilizar en otros servicios. Tu dispositivo recibe un token de acceso privado; el enlace por correo simplemente confirma que eres tú quien inicia sesión.",
    ne: "NullVPN ले पासवर्डबिना प्रमाणीकरण प्रयोग गर्छ — चोरी हुने, चुहिने वा अन्य सेवाहरूमा पुन: प्रयोग हुने कुनै पासवर्ड छैन। तपाईंको यन्त्रले निजी पहुँच टोकन प्राप्त गर्छ; इमेल लिंकले केवल पुष्टि गर्छ कि साँच्चै तपाईं आफैं साइन इन गर्दैनुहुन्छ।",
    fr: "NullVPN utilise une authentification sans mot de passe — aucun mot de passe à voler, fuiter ou réutiliser. Votre appareil reçoit un jeton d\'accès privé ; l\'e-mail est facultatif et sert uniquement à récupérer votre jeton.",
  },
  "terms.h1a": {
    en: "Terms of",
    ru: "Условия",
    fa: "شرایط",
    ar: "شروط",
    es: "Términos",
    ne: "सेवाका",
    fr: "Conditions",
  },
  "terms.h1b": {
    en: "Service",
    ru: "использования",
    fa: "خدمات",
    ar: "الخدمة",
    es: "del Servicio",
    ne: "सर्तहरू",
    fr: "d\'utilisation",
  },
  "terms.updated": {
    en: "Last updated: March 2026",
    ru: "Последнее обновление: март 2026",
    fa: "آخرین به‌روزرسانی: مارس ۲۰۲۶",
    ar: "آخر تحديث: مارس 2026",
    es: "Última actualización: marzo de 2026",
    ne: "अन्तिम अपडेट: मार्च २०२६",
    fr: "Dernière mise à jour : mars 2026",
  },
  "terms.t1": {
    en: "1. Use of Service",
    ru: "1. Использование сервиса",
    fa: "۱. استفاده از سرویس",
    ar: "١. استخدام الخدمة",
    es: "1. Uso del servicio",
    ne: "१. सेवाको प्रयोग",
    fr: "1. Utilisation du service",
  },
  "terms.p1": {
    en: "NullVPN provides private internet access. You agree to use it only for lawful purposes. The service may not be used for illegal activity, hacking, spamming, or any activity violating local laws.",
    ru: "NullVPN предоставляет приватный доступ в интернет. Вы соглашаетесь использовать его только в законных целях. Сервис не может использоваться для незаконной деятельности, взлома, спама или любой деятельности, нарушающей местные законы.",
    fa: "NullVPN دسترسی خصوصی به اینترنت ارائه می‌دهد. موافقت می‌کنید که فقط برای اهداف قانونی از آن استفاده کنید. این سرویس نمی‌تواند برای فعالیت غیرقانونی، هک، اسپم یا هر فعالیتی که قوانین محلی را نقض می‌کند استفاده شود.",
    ar: "يوفر NullVPN وصولاً خاصًا إلى الإنترنت. أنت توافق على استخدامه للأغراض القانونية فقط. لا يجوز استخدام الخدمة للأنشطة غير القانونية أو القرصنة أو البريد العشوائي أو أي نشاط ينتهك القوانين المحلية.",
    es: "NullVPN proporciona acceso privado a internet. Usted acepta utilizarlo únicamente con fines lícitos. El servicio no puede usarse para actividades ilegales, piratería informática, spam ni ninguna actividad que viole las leyes locales.",
    ne: "NullVPN निजी इन्टरनेट पहुँच प्रदान गर्छ। तपाईं यसलाई केवल कानूनी उद्देश्यहरूका लागि मात्र प्रयोग गर्न सहमत हुनुहुन्छ। सेवालाई अवैध गतिविधि, ह्याकिङ, स्प्यामिङ, वा स्थानीय कानूनहरू उल्लंघन गर्ने कुनै पनि गतिविधिका लागि प्रयोग गर्न सकिँदैन।",
    fr: "NullVPN fournit un accès internet privé. Vous acceptez de l\'utiliser uniquement à des fins licites. Le service ne peut pas être utilisé pour des activités illégales, le piratage, le spam ou toute activité violant les lois locales.",
  },
  "terms.t2": {
    en: "2. No Logging",
    ru: "2. Отсутствие логирования",
    fa: "۲. عدم ثبت",
    ar: "٢. عدم الاحتفاظ بالسجلات",
    es: "2. Sin registros",
    ne: "२. कुनै लगिङ छैन",
    fr: "2. Aucune journalisation",
  },
  "terms.p2": {
    en: "NullVPN operates a strict no-logs policy. We do not collect, store, or share any information about your online activity.",
    ru: "NullVPN работает по строгой политике нулевого логирования. Мы не собираем, не храним и не передаём никакую информацию о вашей онлайн-активности.",
    fa: "NullVPN یک سیاست دقیق عدم ثبت را اجرا می‌کند. ما هیچ اطلاعاتی در مورد فعالیت آنلاین شما جمع‌آوری، ذخیره یا به اشتراک نمی‌گذاریم.",
    ar: "يعمل NullVPN وفق سياسة صارمة بعدم الاحتفاظ بالسجلات. لا نجمع أو نخزّن أو نشارك أي معلومات عن نشاطك عبر الإنترنت.",
    es: "NullVPN opera con una estricta política de cero registros. No recopilamos, almacenamos ni compartimos ninguna información sobre su actividad en línea.",
    ne: "NullVPN कडा नो-लग नीति सञ्चालन गर्छ। हामी तपाईंको अनलाइन गतिविधिको बारेमा कुनै जानकारी सङ्कलन, भण्डारण वा साझा गर्दैनौं।",
    fr: "NullVPN applique une politique stricte de zéro log. Nous ne collectons, ne stockons et ne partageons aucune information sur votre activité en ligne.",
  },
  "terms.t3": {
    en: "3. Payments and Refunds",
    ru: "3. Платежи и возвраты",
    fa: "۳. پرداخت‌ها و بازپرداخت‌ها",
    ar: "٣. المدفوعات واسترداد الأموال",
    es: "3. Pagos y reembolsos",
    ne: "३. भुगतान र फिर्ता",
    fr: "3. Paiements et remboursements",
  },
  "terms.p3": {
    en: "Payments are processed by certified third-party providers and are non-refundable except where NullVPN fails to function within 48 hours of purchase. Refund requests must be made via Telegram within the 48-hour window.",
    ru: "Платежи обрабатываются сертифицированными сторонними провайдерами и не подлежат возврату, кроме случаев неработоспособности NullVPN в течение 48 часов после покупки. Заявки на возврат — через Telegram в течение 48 часов.",
    fa: "پرداخت‌ها توسط ارائه‌دهندگان معتبر شخص ثالث پردازش می‌شوند و جز در مواردی که NullVPN تا ۴۸ ساعت پس از خرید کار نکند، غیرقابل استرداد هستند. درخواست استرداد باید در همین بازه ۴۸ ساعته از طریق Telegram ارسال شود.",
    ar: "تتم معالجة المدفوعات عبر مزودين معتمدين من أطراف ثالثة وهي غير قابلة للاسترداد ما لم يتعذر تشغيل NullVPN خلال 48 ساعة من الشراء. يجب إرسال طلبات الاسترداد عبر Telegram خلال مدة الـ48 ساعة.",
    es: "Los pagos son procesados por proveedores externos certificados y no son reembolsables, excepto cuando NullVPN no funciona dentro de las 48 horas posteriores a la compra. Las solicitudes de reembolso deben realizarse por Telegram dentro de ese plazo de 48 horas.",
    ne: "भुक्तानी प्रमाणित तेस्रो-पक्ष प्रदायकहरूमार्फत प्रशोधन हुन्छ र NullVPN किनेको ४८ घण्टाभित्र काम नगरे बाहेक फिर्ता हुँदैन। फिर्ता अनुरोध ४८ घण्टाभित्रै Telegram मार्फत गर्नुपर्छ।",
    fr: "Les paiements sont traités par des prestataires tiers certifiés et ne sont pas remboursables, sauf si NullVPN ne fonctionne pas dans les 48 heures suivant l\'achat. Les demandes de remboursement doivent être faites via Telegram dans ce délai de 48 heures.",
  },
  "terms.t4": {
    en: "4. Account Sharing",
    ru: "4. Общий доступ к аккаунту",
    fa: "۴. اشتراک‌گذاری حساب",
    ar: "٤. مشاركة الحساب",
    es: "4. Compartir la cuenta",
    ne: "४. खाता साझेदारी",
    fr: "4. Partage de compte",
  },
  "terms.p4": {
    en: "Your subscription covers up to 10 simultaneous devices for personal use. Reselling or publicly sharing credentials is not permitted.",
    ru: "Подписка покрывает до 10 одновременных устройств для личного использования. Перепродажа или публичный обмен учётными данными не разрешены.",
    fa: "اشتراک شما تا ۱۰ دستگاه همزمان را برای استفاده شخصی پوشش می‌دهد. فروش مجدد یا اشتراک‌گذاری عمومی اعتبارنامه‌ها مجاز نیست.",
    ar: "يغطي اشتراكك حتى ١٠ أجهزة متزامنة للاستخدام الشخصي. إعادة البيع أو مشاركة بيانات الاعتماد علناً غير مسموح بها.",
    es: "Tu suscripción cubre hasta 10 dispositivos simultáneos para uso personal. No se permite revenderlos ni compartir credenciales públicamente.",
    ne: "तपाईंको सदस्यताले व्यक्तिगत प्रयोगका लागि एकैसाथ १० सम्म उपकरणहरू समेट्छ। पुनर्विक्रय वा सार्वजनिक रूपमा प्रमाणहरू साझेदारी गर्न अनुमति छैन।",
    fr: "Votre abonnement couvre jusqu'à 10 appareils simultanés pour un usage personnel. La revente ou le partage public d'identifiants n'est pas autorisé.",
  },
  "terms.t5": {
    en: "5. Service Availability",
    ru: "5. Доступность сервиса",
    fa: "۵. در دسترس بودن سرویس",
    ar: "٥. توفر الخدمة",
    es: "5. Disponibilidad del servicio",
    ne: "५. सेवा उपलब्धता",
    fr: "5. Disponibilité du service",
  },
  "terms.p5": {
    en: "NullVPN makes no guarantee of 100% uptime but will make reasonable efforts to maintain availability and resolve issues promptly.",
    ru: "NullVPN не гарантирует 100% доступности, но приложит разумные усилия для поддержания работоспособности и оперативного решения проблем.",
    fa: "NullVPN هیچ ضمانتی برای ۱۰۰٪ آپتایم نمی‌دهد اما تلاش معقولی برای حفظ دسترس‌پذیری و رفع سریع مشکلات خواهد کرد.",
    ar: "لا يضمن NullVPN توفرًا بنسبة 100% لكنه سيبذل جهودًا معقولة للحفاظ على التوفر وحل المشكلات سريعًا.",
    es: "NullVPN no garantiza una disponibilidad del 100 %, pero hará esfuerzos razonables para mantenerla y resolver los problemas con prontitud.",
    ne: "NullVPN १००% अपटाइमको ग्यारेन्टी गर्दैन तर उपलब्धता कायम राख्न र समस्याहरू तुरुन्तै समाधान गर्न उचित प्रयास गर्नेछ।",
    fr: "NullVPN ne garantit pas une disponibilité de 100 % mais fera des efforts raisonnables pour la maintenir et résoudre rapidement les problèmes.",
  },
  "terms.t6": {
    en: "6. Changes to Terms",
    ru: "6. Изменения условий",
    fa: "۶. تغییرات در شرایط",
    ar: "٦. تغييرات الشروط",
    es: "6. Cambios en los términos",
    ne: "६. सर्तहरूमा परिवर्तनहरू",
    fr: "6. Modification des conditions",
  },
  "terms.p6": {
    en: "Terms may be updated at any time. Continued use constitutes acceptance. Changes announced via <a href=\"https://t.me/nullvpnnet\" target=\"_blank\" rel=\"noopener\" referrerpolicy=\"no-referrer\">@nullvpnnet</a>.",
    ru: "Условия могут обновляться в любое время. Продолжение использования означает принятие. Изменения объявляются через <a href=\"https://t.me/nullvpnnet\" target=\"_blank\" rel=\"noopener\" referrerpolicy=\"no-referrer\">@nullvpnnet</a>.",
    fa: "شرایط ممکن است در هر زمانی به‌روزرسانی شوند. ادامه استفاده به معنای پذیرش است. تغییرات از طریق <a href=\"https://t.me/nullvpnnet\" target=\"_blank\" rel=\"noopener\" referrerpolicy=\"no-referrer\">@nullvpnnet</a> اعلام می‌شوند.",
    ar: "قد يتم تحديث الشروط في أي وقت. استمرار الاستخدام يعني الموافقة عليها. تُعلن التغييرات عبر <a href=\"https://t.me/nullvpnnet\" target=\"_blank\" rel=\"noopener\" referrerpolicy=\"no-referrer\">@nullvpnnet</a>.",
    es: "Los términos pueden actualizarse en cualquier momento. El uso continuado implica su aceptación. Los cambios se anuncian vía <a href=\"https://t.me/nullvpnnet\" target=\"_blank\" rel=\"noopener\" referrerpolicy=\"no-referrer\">@nullvpnnet</a>.",
    ne: "सर्तहरू जुनसुकै समयमा अपडेट गर्न सकिन्छ। निरन्तर प्रयोगले स्वीकृति गठन गर्छ। परिवर्तनहरू <a href=\"https://t.me/nullvpnnet\" target=\"_blank\" rel=\"noopener\" referrerpolicy=\"no-referrer\">@nullvpnnet</a> मार्फत घोषणा गरिन्छन्।",
    fr: "Les conditions peuvent être mises à jour à tout moment. La poursuite de l'utilisation vaut acceptation. Les changements sont annoncés via <a href=\"https://t.me/nullvpnnet\" target=\"_blank\" rel=\"noopener\" referrerpolicy=\"no-referrer\">@nullvpnnet</a>.",
  },
  "terms.t7": {
    en: "7. Contact",
    ru: "7. Контакт",
    fa: "۷. تماس",
    ar: "٧. التواصل",
    es: "7. Contacto",
    ne: "७. सम्पर्क",
    fr: "7. Contact",
  },
  "terms.p7": {
    en: "Questions? Contact us via Telegram at <a href=\"https://t.me/nullvpnnet\" target=\"_blank\" rel=\"noopener\" referrerpolicy=\"no-referrer\">@nullvpnnet</a>.",
    ru: "Вопросы? Свяжитесь с нами в Telegram: <a href=\"https://t.me/nullvpnnet\" target=\"_blank\" rel=\"noopener\" referrerpolicy=\"no-referrer\">@nullvpnnet</a>.",
    fa: "سوالات؟ از طریق تلگرام در <a href=\"https://t.me/nullvpnnet\" target=\"_blank\" rel=\"noopener\" referrerpolicy=\"no-referrer\">@nullvpnnet</a> با ما تماس بگیرید.",
    ar: "هل لديك أسئلة؟ تواصل معنا عبر Telegram على <a href=\"https://t.me/nullvpnnet\" target=\"_blank\" rel=\"noopener\" referrerpolicy=\"no-referrer\">@nullvpnnet</a>.",
    es: "¿Preguntas? Contáctenos por Telegram en <a href=\"https://t.me/nullvpnnet\" target=\"_blank\" rel=\"noopener\" referrerpolicy=\"no-referrer\">@nullvpnnet</a>.",
    ne: "प्रश्नहरू? <a href=\"https://t.me/nullvpnnet\" target=\"_blank\" rel=\"noopener\" referrerpolicy=\"no-referrer\">@nullvpnnet</a> मा Telegram मार्फत हामीलाई सम्पर्क गर्नुहोस्।",
    fr: "Des questions ? Contactez-nous sur Telegram : <a href=\"https://t.me/nullvpnnet\" target=\"_blank\" rel=\"noopener\" referrerpolicy=\"no-referrer\">@nullvpnnet</a>.",
  },
  "footer.tagline": {
    en: "Private internet for everyone, everywhere.",
    ru: "Приватный интернет для всех, везде.",
    fa: "اینترنت خصوصی برای همه، در همه جا.",
    ar: "إنترنت خاص للجميع، في كل مكان.",
    es: "Internet privado para todos, en todas partes.",
    ne: "सबैका लागि, सर्वत्र निजी इन्टरनेट।",
    fr: "Un internet privé pour tous, partout.",
  },
  "footer.payment": {
    en: "Payments: debit/credit cards via certified partners · crypto (TON, USDT)",
    ru: "Оплата: крипто (TON, USDT и др.) · фиат (ваша локальная валюта)",
    fa: "پرداخت‌ها: کریپتو (TON, USDT و غیره) · فیات (ارز محلی کشور شما)",
    ar: "المدفوعات: بطاقات بنكية عبر شركاء معتمدين · عملات رقمية (TON، USDT)",
    es: "Pagos: tarjetas de débito/crédito vía socios certificados · cripto (TON, USDT)",
    ne: "भुक्तानहरू: क्रिप्टो (TON, USDT, आदि) · फिएट (तपाईंको देशको स्थानीय मुद्रा)",
    fr: "Paiements : cartes bancaires via des partenaires certifiés · crypto (TON, USDT)",
  },
  "footer.pages": {
    en: "Pages",
    ru: "Страницы",
    fa: "صفحات",
    ar: "الصفحات",
    es: "Páginas",
    ne: "पृष्ठहरू",
    fr: "Pages",
  },
  "footer.legal": {
    en: "Legal",
    ru: "Правовые",
    fa: "قانونی",
    ar: "قانوني",
    es: "Legal",
    ne: "कानूनी",
    fr: "Mentions légales",
  },
  "footer.privacy": {
    en: "Privacy Policy",
    ru: "Политика конфиденциальности",
    fa: "سیاست حریم خصوصی",
    ar: "سياسة الخصوصية",
    es: "Política de privacidad",
    ne: "गोपनीयता नीति",
    fr: "Politique de confidentialité",
  },
  "footer.terms": {
    en: "Terms of Service",
    ru: "Условия использования",
    fa: "شرایط خدمات",
    ar: "شروط الخدمة",
    es: "Términos del servicio",
    ne: "सेवाका सर्तहरू",
    fr: "Conditions d'utilisation",
  },
  "footer.copy": {
    en: "© {year} NullVPN. Available on Web2, TON Web3, and all HTTP networks.",
    ru: "© {year} NullVPN. Доступен на Web2, TON Web3 и всех HTTP-сетях.",
    fa: "© {year} NullVPN. در دسترس روی Web2، TON Web3 و همه شبکه‌های HTTP.",
    ar: "© {year} NullVPN. متاح على Web2 وTON Web3 وجميع شبكات HTTP.",
    es: "© {year} NullVPN. Disponible en Web2, TON Web3 y todas las redes HTTP.",
    ne: "© {year} NullVPN. Web2, TON Web3 र सबै HTTP नेटवर्कहरूमा उपलब्ध।",
    fr: "© {year} NullVPN. Disponible sur Web2, TON Web3 et tous les réseaux HTTP.",
  },
  "comp.h1a": {
    en: "NullVPN vs.",
    ru: "NullVPN против",
    fa: "NullVPN در برابر",
    ar: "NullVPN مقابل",
    es: "NullVPN frente al",
    ne: "NullVPN बनाम",
    fr: "NullVPN face aux",
  },
  "comp.h1b": {
    en: "the rest.",
    ru: "остальных.",
    fa: "بقیه.",
    ar: "البقية.",
    es: "resto.",
    ne: "बाँकी।",
    fr: "autres.",
  },
  "comp.sub": {
    en: "An honest comparison for people who actually need their tunnel to keep working on difficult networks.",
    ru: "Честное сравнение для тех, кому действительно нужно, чтобы туннель продолжал работать в сложных сетях.",
    fa: "مقایسه‌ای صادقانه برای کسانی که واقعاً نیاز دارند تونل آن‌ها در شبکه‌های دشوار به کار خود ادامه دهد.",
    ar: "مقارنة صادقة لمن يحتاج فعلًا إلى أن يستمر نفقُه في العمل على الشبكات الصعبة.",
    es: "Una comparación honesta para quienes realmente necesitan que su túnel siga funcionando en redes difíciles.",
    ne: "कठिन नेटवर्कमा आफ्नो टनल निरन्तर काम गर्नुपर्ने मानिसहरूका लागि इमानदार तुलना।",
    fr: "Une comparaison honnête pour celles et ceux qui ont besoin que leur tunnel continue de fonctionner sur les réseaux difficiles.",
  },
  "comp.cta.h": {
    en: "Stop Playing VPN Whack-a-Mole",
    ru: "Хватит играть в «угадай VPN»",
    fa: "دیگر VPN عوض عوض نزنید",
    ar: "توقف عن لعبة القنص مع شبكات VPN",
    es: "Deja de jugar al topo con las VPN",
    ne: "VPN व्ह्याक-ए-मोल खेल्न बन्द गर्नुहोस्",
    fr: "Arrêtez de jouer au VPN whack-a-mole",
  },
  "comp.cta.p": {
    en: "Tired of buying a new VPN subscription every month? Try something architecturally different.",
    ru: "Устали каждый месяц покупать новый VPN? Попробуйте то, что устроено иначе.",
    fa: "هر ماه VPN جدید خریدن خسته شده‌اید؟ چیزی از نظر معماری متفاوت امتحان کنید.",
    ar: "سئمت من شراء اشتراك VPN جديد كل شهر؟ جرّب شيئًا مختلفًا في التصميم نفسه.",
    es: "¿Cansado de comprar una suscripción VPN nueva cada mes? Prueba algo arquitectónicamente diferente.",
    ne: "हर महिना नयाँ VPN सदस्यता किन्न थक्नुभयो? वास्तुकला मा फरक कुनै चीज प्रयास गर्नुहोस्।",
    fr: "Fatigué d'acheter un nouvel abonnement VPN chaque mois ? Essayez quelque chose d'architecturalement différent.",
  },
  "comp.cta.btn": {
    en: "Get NullVPN from $3/month →",
    ru: "NullVPN от 300 ₽/мес →",
    fa: "NullVPN از ۳ دلار/ماه →",
    ar: "احصل على NullVPN ابتداءً من $3 شهريًا →",
    es: "Obtén NullVPN desde $3/mes →",
    ne: "NullVPN $3/महिनाबाट पाउनुहोस् →",
    fr: "Obtenir NullVPN dès $3/mois →",
  },
  "comp.table.feature": {
    en: "Feature",
    ru: "Функция",
    fa: "ویژگی",
    ar: "الميزة",
    es: "Característica",
    ne: "विशेषता",
    fr: "Caractéristique",
  },
  "comp.table.nordvpn": {
    en: "NordVPN",
    ru: "NordVPN",
    fa: "NordVPN",
    ar: "NordVPN",
    es: "NordVPN",
    ne: "NordVPN",
    fr: "NordVPN",
  },
  "comp.table.expressvpn": {
    en: "ExpressVPN",
    ru: "ExpressVPN",
    fa: "ExpressVPN",
    ar: "ExpressVPN",
    es: "ExpressVPN",
    ne: "ExpressVPN",
    fr: "ExpressVPN",
  },
  "comp.table.protonvpn": {
    en: "ProtonVPN",
    ru: "ProtonVPN",
    fa: "ProtonVPN",
    ar: "ProtonVPN",
    es: "ProtonVPN",
    ne: "ProtonVPN",
    fr: "ProtonVPN",
  },
  "comp.table.outline": {
    en: "Self-hosted proxies",
    ru: "Самостоятельные прокси",
    fa: "پراکسی‌های خودمیزبان",
    ar: "بروكسي ذاتية الاستضافة",
    es: "Proxies autoalojados",
    ne: "स्व-होस्ट प्रक्सी",
    fr: "Proxies auto-hébergés",
  },
  "comp.row.nologs": {
    en: "No activity logs (by design)",
    ru: "Нет логов (по архитектуре)",
    fa: "بدون لاگ (طراحی شده)",
    ar: "بلا سجلات نشاط (بالتصميم)",
    es: "No logs (by design)",
    ne: "लगहरू छैनन् (डिजाइन द्वारा)",
    fr: "Aucun journal d'activité (par conception)",
  },
  "comp.row.anonpay": {
    en: "Flexible payment",
    ru: "Анонимная оплата",
    fa: "پرداخت ناشناس",
    ar: "دفع مرن",
    es: "Pago flexible",
    ne: "गुमनाम भुक्तान",
    fr: "Paiement flexible",
  },
  "comp.row.noaccount": {
    en: "Token-based sign-in, no passwords",
    ru: "Вход по токену, без паролей",
    fa: "نیاز به حساب/ایمیل نیست",
    ar: "دخول بالرموز، بلا كلمات مرور",
    es: "No account/email needed",
    ne: "खाता/इमेल आवश्यक छैन",
    fr: "No account/email needed",
  },
  "comp.row.noappstore": {
    en: "No app store required",
    ru: "Без магазина приложений",
    fa: "بدون نیاز به فروشگاه اپ",
    ar: "بلا متجر تطبيقات",
    es: "Sin tienda de aplicaciones",
    ne: "एप स्टोर आवश्यक छैन",
    fr: "Sans magasin d'applications",
  },
  "comp.row.obfuscation": {
    en: "Multi-layer encryption",
    ru: "Многоуровневое шифрование",
    fa: "مبهم‌سازی ترافیک",
    ar: "تشفير متعدد الطبقات",
    es: "Traffic obfuscation",
    ne: "ट्राफिक ओब्फस्केसन",
    fr: "Traffic obfuscation",
  },
  "comp.row.autofailover": {
    en: "Automatic backup routes",
    ru: "Автоматические резервные маршруты",
    fa: "مسیرهای پشتیبان خودکار",
    ar: "مسارات احتياطية تلقائية",
    es: "Rutas de respaldo automáticas",
    ne: "स्वतः ब्याकअप मार्गहरू",
    fr: "Routes de secours automatiques",
  },
  "comp.row.dedicated": {
    en: "Dedicated personal server",
    ru: "Персональный выделенный сервер",
    fa: "سرور شخصی اختصاصی",
    ar: "خادم شخصي مخصص",
    es: "Servidor personal dedicado",
    ne: "समर्पित व्यक्तिगत सर्भर",
    fr: "Serveur personnel dédié",
  },
  "comp.row.reachable": {
    en: "Reachable via Web3 mirror",
    ru: "Доступен через Web3-зеркало",
    fa: "در دسترس اگر سایت مسدود باشد",
    ar: "يمكن الوصول عبر مرآة Web3",
    es: "Accesible vía espejo Web3",
    ne: "साइट असफल भए पनि पहुँचयोग्य",
    fr: "Accessible via le miroir Web3",
  },
  "comp.row.setuptime": {
    en: "Setup time",
    ru: "Время настройки",
    fa: "زمان راه‌اندازی",
    ar: "وقت الإعداد",
    es: "Tiempo de instalación",
    ne: "सेटअप समय",
    fr: "Temps d'installation",
  },
  "comp.val.yes": {
    en: "Yes ✔",
    ru: "Да ✔",
    fa: "بله ✔",
    ar: "نعم ✔",
    es: "Sí ✔",
    ne: "हो ✔",
    fr: "Oui ✔",
  },
  "comp.val.blocked": {
    en: "Struggles ✘",
    ru: "Работает нестабильно ✘",
    fa: "مواجه مشکل ✘",
    ar: "يتعثر ✘",
    es: "Dificultades ✘",
    ne: "समस्या ✘",
    fr: "Rencontre des difficultés ✘",
  },
  "comp.val.unreliable": {
    en: "Unreliable ✘",
    ru: "Ненадёжно ✘",
    fa: "غیرقابل اعتماد ✘",
    ar: "غير موثوق ✘",
    es: "Poco fiable ✘",
    ne: "अविश्वसनीय ✘",
    fr: "Peu fiable ✘",
  },
  "comp.val.partial": {
    en: "Partial",
    ru: "Частично",
    fa: "جزئی",
    ar: "جزئي",
    es: "Parcial",
    ne: "आंशिक",
    fr: "Partiel",
  },
  "comp.val.manual": {
    en: "Manual setup",
    ru: "Ручная настройка",
    fa: "راه‌اندازی دستی",
    ar: "إعداد يدوي",
    es: "Configuración manual",
    ne: "म्यानुअल सेटअप",
    fr: "Configuration manuelle",
  },
  "comp.val.policyonly": {
    en: "Policy only",
    ru: "Только политика",
    fa: "فقط سیاست",
    ar: "سياسة فقط",
    es: "Solo por política",
    ne: "केवल नीति",
    fr: "Politique seulement",
  },
  "comp.val.cardpaypal": {
    en: "Card/PayPal",
    ru: "Карта/PayPal ✘",
    fa: "کارت/PayPal ✘",
    ar: "بطاقة/PayPal",
    es: "Tarjeta/PayPal",
    ne: "कार्ड/PayPal ✘",
    fr: "Carte/PayPal",
  },
  "comp.val.ton": {
    en: "Debit/credit cards · Crypto ✔",
    ru: "TON крипта ✔",
    fa: "کریپتو TON ✔",
    ar: "بطاقات بنكية · عملات رقمية ✔",
    es: "Tarjetas · Cripto ✔",
    ne: "TON क्रिप्टो ✔",
    fr: "Cartes bancaires · Crypto ✔",
  },
  "comp.val.required": {
    en: "Required ✘",
    ru: "Требуется ✘",
    fa: "الزامی ✘",
    ar: "إلزامي ✘",
    es: "Obligatorio ✘",
    ne: "आवश्यक ✘",
    fr: "Obligatoire ✘",
  },
  "comp.val.depends": {
    en: "Depends",
    ru: "Зависит",
    fa: "بستگی دارد",
    ar: "يعتمد",
    es: "Depende",
    ne: "निर्भर गर्छ",
    fr: "Cela dépend",
  },
  "comp.val.appstore": {
    en: "App store ✘",
    ru: "Магазин приложений ✘",
    fa: "فروشگاه اپ ✘",
    ar: "متجر تطبيقات ✘",
    es: "Tienda de apps ✘",
    ne: "एप स्टोर ✘",
    fr: "Magasin d'apps ✘",
  },
  "comp.varies": {
    en: "Varies",
    ru: "Разнится",
    fa: "متفاوت است",
    ar: "يختلف",
    es: "Varía",
    ne: "भिन्न हुन्छ",
    fr: "Variable",
  },
  "comp.val.deep": {
    en: "Deep ✔",
    ru: "Глубокая ✔",
    fa: "عمیق ✔",
    ar: "عميق ✔",
    es: "Profundo ✔",
    ne: "गहिरो ✔",
    fr: "Poussé ✔",
  },
  "comp.val.obfservers": {
    en: "Multi-layer ✔",
    ru: "Многоуровневое ✔",
    fa: "سرورهای مبهم‌شده",
    ar: "متعدد الطبقات ✔",
    es: "Obfuscated servers",
    ne: "ओब्फस्केटेड सर्भरहरू",
    fr: "Obfuscated servers",
  },
  "comp.val.lightway": {
    en: "Lightway",
    ru: "Lightway",
    fa: "Lightway",
    ar: "Lightway",
    es: "Lightway",
    ne: "लाइटवे",
    fr: "Lightway",
  },
  "comp.val.stealth": {
    en: "Stealth",
    ru: "Stealth",
    fa: "Stealth",
    ar: "Stealth",
    es: "Stealth",
    ne: "स्टील्थ",
    fr: "Stealth",
  },
  "comp.val.some": {
    en: "Some",
    ru: "Некоторая",
    fa: "برخی",
    ar: "بعضها",
    es: "Algunos",
    ne: "केही",
    fr: "Certains",
  },
  "comp.val.no": {
    en: "No ✘",
    ru: "Нет ✘",
    fa: "نه ✘",
    ar: "لا ✘",
    es: "No ✘",
    ne: "होइन ✘",
    fr: "Non ✘",
  },
  "comp.val.shared": {
    en: "Shared ✘",
    ru: "Общий ✘",
    fa: "مشترک ✘",
    ar: "مشترك ✘",
    es: "Compartido ✘",
    ne: "साझा ✘",
    fr: "Partagé ✘",
  },
  "comp.val.selfhosted": {
    en: "Self-hosted",
    ru: "Самостоятельный хостинг",
    fa: "میزبانی خود",
    ar: "استضافة ذاتية",
    es: "Autoalojado",
    ne: "स्व-होस्ट गरिएको",
    fr: "Auto-hébergé",
  },
  "comp.val.telegramweb3": {
    en: "Telegram + Web3 ✔",
    ru: "Telegram + Web3 ✔",
    fa: "تلگرام + Web3 ✔",
    ar: "Telegram + Web3 ✔",
    es: "Telegram + Web3 ✔",
    ne: "Telegram + Web3 ✔",
    fr: "Telegram + Web3 ✔",
  },
  "comp.val.websiteonly": {
    en: "Website only ✘",
    ru: "Только сайт ✘",
    fa: "فقط وب‌سایت ✘",
    ar: "الموقع فقط ✘",
    es: "Solo web ✘",
    ne: "केवल वेबसाइट ✘",
    fr: "Site web seulement ✘",
  },
  "comp.val.cardoutline": {
    en: "Card ✘",
    ru: "Карта ✘",
    fa: "کارت ✘",
    ar: "بطاقة ✘",
    es: "Tarjeta ✘",
    ne: "कार्ड ✘",
    fr: "Carte ✘",
  },
  "comp.val.directapk": {
    en: "Direct APK ✔",
    ru: "Прямой APK ✔",
    fa: "APK مستقیم ✔",
    ar: "APK مباشر ✔",
    es: "APK directo ✔",
    ne: "प्रत्यक्ष APK ✔",
    fr: "APK direct ✔",
  },
  "comp.val.seconds60": {
    en: "60 seconds",
    ru: "60 секунд",
    fa: "۶۰ ثانیه",
    ar: "60 ثانية",
    es: "60 segundos",
    ne: "६० सेकेन्ड",
    fr: "60 secondes",
  },
  "comp.val.minutes5": {
    en: "5+ min",
    ru: "5+ мин",
    fa: "+۵ دقیقه",
    ar: "5+ دقائق",
    es: "5+ min",
    ne: "+५ मिनेट",
    fr: "5+ min",
  },
  "comp.val.hours": {
    en: "Hours (manual)",
    ru: "Часы (вручную)",
    fa: "ساعت‌ها (دستی)",
    ar: "ساعات (يدويًا)",
    es: "Horas (manual)",
    ne: "घण्टा (म्यानुअल)",
    fr: "Heures (manuel)",
  },
  "comp.note.h": {
    en: "Why NullVPN is built differently",
    ru: "Почему NullVPN устроен иначе",
    fa: "چرا NullVPN متفاوت ساخته شده است",
    ar: "لماذا صُمم NullVPN بشكل مختلف",
    es: "Por qué NullVPN está construido diferente",
    ne: "NullVPN किन फरक रूपमा बनाइएको हो",
    fr: "Pourquoi NullVPN est conçu différemment",
  },
  "comp.note.p1": {
    en: "Consumer VPNs are built for general privacy in open markets. They route many users through shared servers, and they are not optimised for difficult network environments.",
    ru: "Потребительские VPN созданы для общей приватности на открытых рынках. Они ведут многих пользователей через общие серверы и не оптимизированы для сложных сетевых сред.",
    fa: "VPNهای مصرفی برای حریم خصوصی عمومی در بازارهای آزاد ساخته شده‌اند. آن‌ها ترافیک کاربران را از سرورهای مشترک عبور می‌دهند و برای محیط‌های دشوار شبکه بهینه نشده‌اند.",
    ar: "شبكات VPN الاستهلاكية مبنية للخصوصية العامة في الأسواق المفتوحة. تمرر عددًا كبيرًا من المستخدمين عبر خوادم مشتركة، وهي غير محسّنة لبيئات الشبكات الصعبة.",
    es: "Las VPN de consumo están pensadas para la privacidad general en mercados abiertos. Dirigen a muchos usuarios por servidores compartidos y no están optimizadas para entornos de red difíciles.",
    ne: "उपभोक्ता VPN हरू खुला बजारमा सामान्य गोपनीयताका लागि बनाइएका हुन्। तिनीहरू धेरै प्रयोगकर्तालाई साझा सर्भरबाट पठाउँछन् र कठिन सञ्जाल वातावरणका लागि अनुकूलित छैनन्।",
    fr: "Les VPN grand public sont conçus pour la vie privée générale sur des marchés ouverts. Ils font transiter de nombreux utilisateurs via des serveurs mutualisés et ne sont pas optimisés pour les environnements réseau difficiles.",
  },
  "comp.note.p2": {
    en: "NullVPN is designed from the ground up for one purpose: a reliable private tunnel that keeps working on any network — mobile, fixed, public, or restrictive. Every design decision flows from that single goal.",
    ru: "NullVPN создан с нуля ради одной цели: надёжный приватный туннель, который работает в любой сети — мобильной, домашней, публичной или закрытой. Каждое решение исходит из этой цели.",
    fa: "NullVPN از پایه با یک هدف طراحی شده است: تونل خصوصی قابل اعتمادی که روی هر شبکه‌ای — موبایل، ثابت، عمومی یا محدود — به کار خود ادامه می‌دهد. هر تصمیم طراحی از همان هدف سرچشمه می‌گیرد.",
    ar: "صُمم NullVPN من الأساس لهدف واحد: نفق خاص موثوق يستمر في العمل على أي شبكة — جوال أو ثابت أو عام أو مقيد. كل قرار في التصميم ينبع من هذا الهدف الوحيد.",
    es: "NullVPN está diseñado desde cero con un único propósito: un túnel privado y fiable que sigue funcionando en cualquier red: móvil, fija, pública o restrictiva. Cada decisión de diseño parte de ese objetivo.",
    ne: "NullVPN एउटै उद्देश्यका लागि सुरुदेखि डिजाइन गरिएको हो: कुनै पनि सञ्जाल—मोबाइल, स्थिर, सार्वजनिक वा प्रतिबन्धित—मा निरन्तर काम गर्ने भरपर्दो निजी टनेल। हरेक डिजाइन निर्णय त्यही लक्ष्यबाट आउँछ।",
    fr: "NullVPN est conçu dès l’origine pour un seul objectif : un tunnel privé fiable qui continue de fonctionner sur tout réseau — mobile, fixe, public ou restrictif. Chaque choix de conception découle de cet unique but.",
  },
  "footer.refund": {
    en: "Refund Policy",
    ru: "Возврат средств",
    fa: "سیاست بازگشت",
    ar: "سياسة استرداد الأموال",
    es: "Política de reembolso",
    ne: "फिर्ता नीति",
    fr: "Politique de remboursement",
  },
  "refund.h1a": {
    en: "Refund",
    ru: "Политика",
    fa: "سیاست",
    ar: "سياسة",
    es: "Política",
    ne: "फिर्ता",
    fr: "Politique",
  },
  "refund.h1b": {
    en: "Policy",
    ru: "возврата",
    fa: "بازگشت",
    ar: "الاسترداد",
    es: "de reembolso",
    ne: "नीति",
    fr: "de remboursement",
  },
  "refund.updated": {
    en: "Last updated: October 2026",
    ru: "Обновлено: октябрь 2026",
    fa: "آخرین به‌روزرسانی: اکتبر ۲۰۲۶",
    ar: "آخر تحديث: أكتوبر ٢٠٢٦",
    es: "Última actualización: octubre de 2026",
    ne: "अन्तिम अद्यावधिक: अक्टोबर २०२६",
    fr: "Dernière mise à jour : octobre 2026",
  },
  "refund.intro": {
    en: "One simple rule. If NullVPN does not work for you, you get your money back.",
    ru: "Одно простое правило. Если NullVPN у вас не работает — мы вернём деньги.",
    fa: "یک قانون ساده. اگر NullVPN برای شما کار نکند، پول شما برمی‌گردد.",
    ar: "قاعدة واحدة بسيطة. إذا لم يعمل NullVPN لديك، تستعيد أموالك.",
    es: "Una regla sencilla. Si NullVPN no funciona para usted, recupera su dinero.",
    ne: "एक सरल नियम। NullVPN तपाईंको लागि काम नगरे, तपाईंको पैसा फिर्ता हुन्छ।",
    fr: "Une règle simple. Si NullVPN ne fonctionne pas pour vous, vous êtes remboursé.",
  },
  "refund.rule.h": {
    en: "The 48-hour rule",
    ru: "Правило 48 часов",
    fa: "قانون ۴۸ ساعت",
    ar: "قاعدة الـ48 ساعة",
    es: "La regla de 48 horas",
    ne: "४८ घण्टाको नियम",
    fr: "La règle des 48 heures",
  },
  "refund.rule.p": {
    en: "If NullVPN does not work in your location within 48 hours of purchase, message us on Telegram for a full refund. No questions asked.",
    ru: "Если NullVPN не работает в вашем месте в течение 48 часов после покупки, свяжитесь с нами в Telegram для полного возврата средств. Без вопросов.",
    fa: "اگر NullVPN در موقعیت شما در عرض ۴۸ ساعت پس از خرید کار نکرد، برای بازپرداخت کامل با ما در تلگرام تماس بگیرید. بدون سوال.",
    ar: "إذا لم يعمل NullVPN في موقعك خلال 48 ساعة من الشراء، راسلنا على تيليجرام لاسترداد كامل المبلغ. بدون أسئلة.",
    es: "Si NullVPN no funciona en tu ubicación dentro de las 48 horas posteriores a la compra, escríbenos por Telegram para un reembolso completo. Sin preguntas.",
    ne: "यदि खरिद गरेको ४८ घण्टाभित्र तपाईंको स्थानमा NullVPN काम गर्दैन भने, पूर्ण फिर्ताका लागि Telegram मा हामीलाई सम्पर्क गर्नुहोस्। कुनै प्रश्न सोधिँदैन।",
    fr: "Si NullVPN ne fonctionne pas chez vous dans les 48 heures suivant l'achat, écrivez-nous sur Telegram pour un remboursement complet. Sans questions.",
  },
  "refund.how.h": {
    en: "How to request",
    ru: "Как запросить",
    fa: "نحوه درخواست",
    ar: "كيفية الطلب",
    es: "Cómo solicitarlo",
    ne: "अनुरोध कसरी गर्ने",
    fr: "Comment demander",
  },
  "refund.how.p": {
    en: "Message <a href=\"https://t.me/nullvpnnetbot\" target=\"_blank\" rel=\"noopener\" referrerpolicy=\"no-referrer\">@nullvpnnetbot</a> on Telegram (or <a href=\"https://t.me/nullvpnnet\" target=\"_blank\" rel=\"noopener\" referrerpolicy=\"no-referrer\">@nullvpnnet</a>) with your purchase details. We reply as quickly as we can.",
    ru: "Напишите <a href=\"https://t.me/nullvpnnetbot\" target=\"_blank\" rel=\"noopener\" referrerpolicy=\"no-referrer\">@nullvpnnetbot</a> в Telegram (или <a href=\"https://t.me/nullvpnnet\" target=\"_blank\" rel=\"noopener\" referrerpolicy=\"no-referrer\">@nullvpnnet</a>) с деталями покупки. Отвечаем как можно быстрее.",
    fa: "به <a href=\"https://t.me/nullvpnnetbot\" target=\"_blank\" rel=\"noopener\" referrerpolicy=\"no-referrer\">@nullvpnnetbot</a> در تلگرام (یا <a href=\"https://t.me/nullvpn_net\" target=\"_blank\" rel=\"noopener\" referrerpolicy=\"no-referrer\">@nullvpn_net</a>) همراه با جزئیات خریدتان پیام دهید. در اسرع وقت پاسخ می‌دهیم.",
    ar: "راسل <a href=\"https://t.me/nullvpnnetbot\" target=\"_blank\" rel=\"noopener\" referrerpolicy=\"no-referrer\">@nullvpnnetbot</a> على تيليجرام (أو <a href=\"https://t.me/nullvpn_net\" target=\"_blank\" rel=\"noopener\" referrerpolicy=\"no-referrer\">@nullvpn_net</a>) مع تفاصيل عملية الشراء. نرد بأسرع ما يمكن.",
    es: "Escriba a <a href=\"https://t.me/nullvpnnetbot\" target=\"_blank\" rel=\"noopener\" referrerpolicy=\"no-referrer\">@nullvpnnetbot</a> por Telegram (o a <a href=\"https://t.me/nullvpn_net\" target=\"_blank\" rel=\"noopener\" referrerpolicy=\"no-referrer\">@nullvpn_net</a>) con los detalles de su compra. Respondemos lo antes posible.",
    ne: "किन्ने विवरणसहित Telegram मा <a href=\"https://t.me/nullvpnnetbot\" target=\"_blank\" rel=\"noopener\" referrerpolicy=\"no-referrer\">@nullvpnnetbot</a> (वा <a href=\"https://t.me/nullvpn_net\" target=\"_blank\" rel=\"noopener\" referrerpolicy=\"no-referrer\">@nullvpn_net</a>) लाई मेसेज गर्नुहोस्। हामी सकेसम्म चाँडो जवाफ दिन्छौं।",
    fr: "Écrivez à <a href=\"https://t.me/nullvpnnetbot\" target=\"_blank\" rel=\"noopener\" referrerpolicy=\"no-referrer\">@nullvpnnetbot</a> sur Telegram (ou à <a href=\"https://t.me/nullvpn_net\" target=\"_blank\" rel=\"noopener\" referrerpolicy=\"no-referrer\">@nullvpn_net</a>) avec les détails de votre achat. Nous répondons au plus vite.",
  },
  "refund.method.h": {
    en: "How you get the money",
    ru: "Как возвращаются деньги",
    fa: "چگونه پول برمی‌گردد",
    ar: "كيف تستعيد أموالك",
    es: "Cómo recibes el dinero",
    ne: "पैसा कसरी फिर्ता हुन्छ",
    fr: "Comment vous êtes remboursé",
  },
  "refund.method.p": {
    en: "Refunds are returned to the original payment method through the payment provider that processed the transaction. Payment mechanics are handled by our certified payment partners.",
    ru: "Возврат осуществляется на исходный способ оплаты через платёжного провайдера, который обрабатывал транзакцию. Механику возврата выполняют наши сертифицированные платёжные партнёры.",
    fa: "مبلغ استرداد از طریق ارائه‌دهنده پرداختی که تراکنش را پردازش کرده به روش پرداخت اصلی برمی‌گردد. مکانیزم پرداخت را شرکای معتبر پرداخت ما انجام می‌دهند.",
    ar: "يُعاد مبلغ الاسترداد إلى وسيلة الدفع الأصلية عبر مزود الدفع الذي عالج المعاملة. تتولى آلية الدفع شركاء الدفع المعتمدون لدينا.",
    es: "Los reembolsos se devuelven al método de pago original a través del proveedor de pago que procesó la transacción. La mecánica del pago la gestionan nuestros proveedores de pago certificados.",
    ne: "फिर्ता कारोबार प्रशोधन गर्ने भुक्तानी प्रदायकमार्फत मूल भुक्तानी विधिमै फर्किन्छ। भुक्तानी प्रक्रिया हाम्रा प्रमाणित भुक्तानी साझेदारहरूले सम्हाल्छन्।",
    fr: "Les remboursements sont effectués sur le moyen de paiement d\'origine via le prestataire de paiement qui a traité la transaction. La mécanique de paiement est gérée par nos partenaires certifiés.",
  },
  "refund.excl.h": {
    en: "What is not covered",
    ru: "Что не покрывается",
    fa: "چه مواردی پوشش داده نمی‌شود",
    ar: "ما لا يشمله الاسترداد",
    es: "Qué no está cubierto",
    ne: "के छैन समेटिएको",
    fr: "Ce qui n'est pas couvert",
  },
  "refund.excl.p": {
    en: "Refunds are not available after the 48-hour window or where the service is functioning. Payments are otherwise non-refundable as described in the Terms of Service.",
    ru: "Возврат недоступен по истечении 48 часов или если сервис работает. В остальных случаях платежи не возвращаются — подробнее в Условиях использования.",
    fa: "پس از بازه ۴۸ ساعته یا وقتی سرویس درست کار می‌کند، استرداد ممکن نیست. در غیر این صورت پرداخت‌ها طبق شرایط استفاده از سرویس غیرقابل استرداد هستند.",
    ar: "لا يتوفر استرداد بعد مهلة الـ48 ساعة أو عندما تكون الخدمة تعمل. عدا ذلك، المدفوعات غير قابلة للاسترداد كما هو موضح في شروط الخدمة.",
    es: "No hay reembolsos después del plazo de 48 horas ni cuando el servicio funciona. En lo demás, los pagos no son reembolsables según se describe en los Términos del Servicio.",
    ne: "४८ घण्टा नाघेपछि वा सेवा राम्रोसँग चलिरहेको अवस्थामा फिर्ता उपलब्ध हुँदैन। अन्यथा भुक्तानी सेवा सर्तहरूमा उल्लेख भएअनुसार फिर्ता हुँदैन।",
    fr: "Aucun remboursement après le délai de 48 heures ni lorsque le service fonctionne. Sinon, les paiements ne sont pas remboursables, comme décrit dans les Conditions d\'utilisation.",
  },
  "refund.cta.btn": {
    en: "Request a refund on Telegram →",
    ru: "Запросить возврат в Telegram →",
    fa: "درخواست بازگشت وجه در تلگرام →",
    ar: "اطلب استرداد الأموال على تيليجرام →",
    es: "Solicitar reembolso por Telegram →",
    ne: "Telegram मा फिर्ता अनुरोध गर्नुहोस् →",
    fr: "Demander un remboursement sur Telegram →",
  },
  "refund.terms.link": {
    en: "Read the full Terms of Service →",
    ru: "Читать полные условия →",
    fa: "مطالعه کامل شرایط استفاده →",
    ar: "اقرأ كامل شروط الخدمة →",
    es: "Leer los Términos de Servicio completos →",
    ne: "पूर्ण सेवा सर्तहरू पढ्नुहोस् →",
    fr: "Lire les Conditions de Service complètes →",
  },
  "terms.t8": {
    en: "8. Local Laws and Network Policies",
    ru: "8. Местные законы и политики сетей",
    fa: "۸. قوانین محلی و سیاست‌های شبکه",
    ar: "٨. القوانين المحلية وسياسات الشبكات",
    es: "8. Leyes locales y políticas de red",
    ne: "८. स्थानीय कानून र नेटवर्क नीतिहरू",
    fr: "8. Lois locales et politiques réseau",
  },
  "terms.p8": {
    en: "Some networks or jurisdictions may restrict VPN usage. You are responsible for complying with local laws and the terms of your network provider.",
    ru: "Некоторые сети или юрисдикции могут ограничивать использование VPN. Вы отвечаете за соблюдение местных законов и правил вашего сетевого провайдера.",
    fa: "برخی شبکه‌ها یا حوزه‌های قضایی ممکن است استفاده از VPN را محدود کنند. رعایت قوانین محلی و شرایط ارائه‌دهنده شبکه شما بر عهده خودتان است.",
    ar: "قد تقيّد بعض الشبكات أو الولايات القضائية استخدام VPN. أنت مسؤول عن الالتزام بالقوانين المحلية وشروط مزود الشبكة لديك.",
    es: "Algunas redes o jurisdicciones pueden restringir el uso de VPN. Usted es responsable de cumplir las leyes locales y los términos de su proveedor de red.",
    ne: "केही नेटवर्क वा क्षेत्राधिकारले VPN प्रयोग सीमित गर्न सक्छ। स्थानीय कानुन र तपाईंको नेटवर्क प्रदायकका सर्तहरू पालना गर्ने जिम्मेवारी तपाईंको हो।",
    fr: "Certains réseaux ou juridictions peuvent restreindre l\'usage des VPN. Vous êtes responsable du respect des lois locales et des conditions de votre fournisseur d\'accès.",
  },
  "terms.related": {
    en: "Related:",
    ru: "См. также:",
    fa: "همچنین ببینید:",
    ar: "ذو الصلة:",
    es: "Relacionados:",
    ne: "सम्बन्धित:",
    fr: "Liés :",
  },
  "priv.tbl.h": {
    en: "What data exists — and who can see it",
    ru: "Какие данные есть — и кто их видит",
    fa: "چه داده‌هایی وجود دارند — و چه کسی می‌تواند آن‌ها را ببیند",
    ar: "ما البيانات الموجودة — ومن يمكنه رؤيتها",
    es: "Qué datos existen — y quién puede verlos",
    ne: "कुन डेटा अवस्थित छ — र कसले हेर्न सक्छ",
    fr: "Quelles données existent — et qui peut les voir",
  },
  "priv.tbl.intro": {
    en: "We minimize what is needed to run accounts, subscriptions, payments, security, and support. Here is the honest, itemized picture instead of slogans.",
    ru: "Мы минимизируем данные, нужные для работы аккаунтов, подписок, платежей, безопасности и поддержки. Вот честная детализация вместо лозунгов.",
    fa: "آنچه برای راه‌اندازی حساب‌ها، اشتراک‌ها، پرداخت‌ها، امنیت و پشتیبانی لازم است را به حداقل می‌رسانیم. این تصویر صادقانه و موردی است، نه شعار.",
    ar: "نقلل إلى الحد الأدنى ما يلزم لتشغيل الحسابات والاشتراكات والمدفوعات والأمان والدعم. إليك الصورة الصادقة المفصلة بدلًا من الشعارات.",
    es: "Minimizamos lo necesario para operar cuentas, suscripciones, pagos, seguridad y soporte. Esta es la imagen honesta y detallada, sin eslóganes.",
    ne: "खाता, सदस्यता, भुक्तानी, सुरक्षा र सहयोग चलाउन आवश्यक पर्ने कुरा हामी न्यूनतममा झार्छौं। नाराको सट्टा यहाँ इमानदार, वस्तुगत तस्बिर छ।",
    fr: "Nous minimisons ce qui est nécessaire pour gérer comptes, abonnements, paiements, sécurité et support. Voici le tableau honnête et détaillé, sans slogans.",
  },
  "priv.tbl.c1": {
    en: "Data",
    ru: "Данные",
    fa: "داده‌ها",
    ar: "البيانات",
    es: "Datos",
    ne: "डाटा",
    fr: "Données",
  },
  "priv.tbl.c2": {
    en: "Where it lives",
    ru: "Где хранится",
    fa: "کجا ذخیره می‌شود",
    ar: "أين يُخزَّن",
    es: "Dónde se guarda",
    ne: "कहाँ रहन्छ",
    fr: "Où il est conservé",
  },
  "priv.tbl.c3": {
    en: "Why",
    ru: "Зачем",
    fa: "چرا",
    ar: "لماذا",
    es: "Por qué",
    ne: "किन",
    fr: "Pourquoi",
  },
  "priv.tbl.c4": {
    en: "Retention",
    ru: "Хранение",
    fa: "مدت نگهداری",
    ar: "مدة الاحتفاظ",
    es: "Retención",
    ne: "सुरक्षित राख्ने अवधि",
    fr: "Conservation",
  },
  "priv.tbl.r1.d": {
    en: "Traffic content and browsing activity",
    ru: "Содержимое трафика и история посещений",
    fa: "محتوای ترافیک و فعالیت مرور",
    ar: "محتوى حركة البيانات ونشاط التصفح",
    es: "Contenido del tráfico y actividad de navegación",
    ne: "ट्राफिक सामग्री र ब्राउजिङ गतिविधि",
    fr: "Contenu du trafic et activité de navigation",
  },
  "priv.tbl.r1.w": {
    en: "Not retained — tunnel exits run without traffic or connection logs",
    ru: "Не сохраняется — на выходных узлах нет логов трафика и соединений",
    fa: "نگهداری نمی‌شود — خروجی‌های تونل بدون لاگ ترافیک یا اتصال کار می‌کنند",
    ar: "غير محفوظ — مخرجات النفق تعمل بدون سجلات بيانات أو اتصالات",
    es: "No se retiene — las salidas del túnel funcionan sin registros de tráfico ni de conexiones",
    ne: "राखिँदैन — टनेल निकासहरू ट्राफिक वा जडान लगबिना चल्छन्",
    fr: "Non conservé — les sorties de tunnel fonctionnent sans logs de trafic ni de connexion",
  },
  "priv.tbl.r1.y": {
    en: "—",
    ru: "—",
    fa: "—",
    ar: "—",
    es: "—",
    ne: "—",
    fr: "—",
  },
  "priv.tbl.r1.rt": {
    en: "Nothing to retain",
    ru: "Хранить нечего",
    fa: "چیزی برای نگهداری نیست",
    ar: "لا شيء لحفظه",
    es: "Nada que retener",
    ne: "राख्नुपर्ने केही छैन",
    fr: "Rien à conserver",
  },
  "priv.tbl.r2.d": {
    en: "Account identifier (private access token, optional email)",
    ru: "Идентификатор аккаунта (приватный токен доступа, опциональный email)",
    fa: "شناسه حساب (توکن دسترسی خصوصی، ایمیل اختیاری)",
    ar: "معرّف الحساب (رمز وصول خاص، بريد إلكتروني اختياري)",
    es: "Identificador de cuenta (token de acceso privado, correo opcional)",
    ne: "खाता पहिचानकर्ता (निजी पहुँच टोकन, ऐच्छिक इमेल)",
    fr: "Identifiant de compte (jeton d\'accès privé, e-mail facultatif)",
  },
  "priv.tbl.r2.w": {
    en: "NullVPN account backend",
    ru: "Бэкенд аккаунтов NullVPN",
    fa: "بک‌اند حساب‌های NullVPN",
    ar: "الخلفية البرمجية لحسابات NullVPN",
    es: "Backend de cuentas de NullVPN",
    ne: "NullVPN खाता ब्याकएन्ड",
    fr: "Backend de comptes NullVPN",
  },
  "priv.tbl.r2.y": {
    en: "Authentication, subscription binding, recovery links",
    ru: "Аутентификация, привязка подписки, ссылки восстановления",
    fa: "احراز هویت، اتصال اشتراک، لینک‌های بازیابی",
    ar: "المصادقة وربط الاشتراك وروابط الاستعادة",
    es: "Autenticación, vinculación de suscripción, enlaces de recuperación",
    ne: "प्रमाणीकरण, सदस्यता जोड्ने, पुनःप्राप्ति लिंकहरू",
    fr: "Authentification, liaison d\'abonnement, liens de récupération",
  },
  "priv.tbl.r2.rt": {
    en: "Life of the account",
    ru: "Время жизни аккаунта",
    fa: "طول عمر حساب",
    ar: "طوال عمر الحساب",
    es: "Vida de la cuenta",
    ne: "खाताको आयु",
    fr: "Durée de vie du compte",
  },
  "priv.tbl.r3.d": {
    en: "Payment confirmation (amount, method, transaction reference)",
    ru: "Подтверждение платежа (сумма, способ, ссылка на транзакцию)",
    fa: "تأیید پرداخت (مبلغ، روش، شناسه تراکنش)",
    ar: "تأكيد الدفع (المبلغ والطريقة ومرجع المعاملة)",
    es: "Confirmación de pago (importe, método, referencia de la transacción)",
    ne: "भुक्तानी पुष्टि (रकम, विधि, कारोबार सन्दर्भ)",
    fr: "Confirmation de paiement (montant, méthode, référence de transaction)",
  },
  "priv.tbl.r3.w": {
    en: "Certified payment partners; NullVPN sees only a success confirmation",
    ru: "Сертифицированные платёжные партнёры; NullVPN видит только подтверждение успеха",
    fa: "شرکای پرداخت معتبر؛ NullVPN فقط تأیید موفقیت را می‌بیند",
    ar: "شركاء دفع معتمدون؛ يرى NullVPN تأكيد النجاح فقط",
    es: "Proveedores de pago certificados; NullVPN solo ve una confirmación de éxito",
    ne: "प्रमाणित भुक्तानी साझेदारहरू; NullVPN ले सफलताको पुष्टि मात्र देख्छ",
    fr: "Partenaires de paiement certifiés ; NullVPN ne voit qu\'une confirmation de succès",
  },
  "priv.tbl.r3.y": {
    en: "Reconciliation and refunds",
    ru: "Сверка платежей и возвраты",
    fa: "مغایرت‌گیری و استردادها",
    ar: "التسوية واسترداد الأموال",
    es: "Conciliación y reembolsos",
    ne: "मिलान र फिर्ता",
    fr: "Réconciliation et remboursements",
  },
  "priv.tbl.r3.rt": {
    en: "Per provider policy and accounting rules",
    ru: "По политике провайдера и правилам бухучёта",
    fa: "طبق سیاست ارائه‌دهنده و قواعد حسابداری",
    ar: "حسب سياسة المزود والقواعد المحاسبية",
    es: "Según la política del proveedor y las normas contables",
    ne: "प्रदायक नीति र लेखा नियमअनुसार",
    fr: "Selon la politique du prestataire et les règles comptables",
  },
  "priv.tbl.r4.d": {
    en: "Approximate traffic volume per billing period",
    ru: "Примерный объём трафика за расчётный период",
    fa: "حجم تقریبی ترافیک در هر دوره صورتحساب",
    ar: "حجم البيانات التقريبي لكل دورة فوترة",
    es: "Volumen aproximado de tráfico por periodo de facturación",
    ne: "प्रति बिलिङ अवधि अनुमानित ट्राफिक परिमाण",
    fr: "Volume de trafic approximatif par période de facturation",
  },
  "priv.tbl.r4.w": {
    en: "NullVPN backend",
    ru: "Бэкенд NullVPN",
    fa: "بک‌اند NullVPN",
    ar: "خلفية NullVPN البرمجية",
    es: "Backend de NullVPN",
    ne: "NullVPN ब्याकएन्ड",
    fr: "Backend NullVPN",
  },
  "priv.tbl.r4.y": {
    en: "Plan operation and abuse prevention",
    ru: "Работа тарифа и защита от злоупотреблений",
    fa: "کارکرد پلن و جلوگیری از سوءاستفاده",
    ar: "تشغيل الخطة ومنع الإساءة",
    es: "Operación del plan y prevención de abusos",
    ne: "प्लान सञ्चालन र दुरुपयोग रोकथाम",
    fr: "Fonctionnement de l\'offre et prévention des abus",
  },
  "priv.tbl.r4.rt": {
    en: "Billing period",
    ru: "Расчётный период",
    fa: "دوره صورتحساب",
    ar: "دورة الفوترة",
    es: "Periodo de facturación",
    ne: "बिलिङ अवधि",
    fr: "Période de facturation",
  },
  "priv.tbl.r5.d": {
    en: "Connection events log",
    ru: "Журнал событий подключения",
    fa: "لاگ رخدادهای اتصال",
    ar: "سجل أحداث الاتصال",
    es: "Registro de eventos de conexión",
    ne: "जडान घटना लग",
    fr: "Journal des événements de connexion",
  },
  "priv.tbl.r5.w": {
    en: "Your own device only — a local ring buffer that is never uploaded",
    ru: "Только ваше устройство — локальный кольцевой буфер, никогда не выгружается",
    fa: "فقط روی دستگاه خودتان — بافر حلقوی محلی که هرگز آپلود نمی‌شود",
    ar: "على جهازك فقط — مخزن حلقي محلي لا يُرفع أبدًا",
    es: "Solo su propio dispositivo — un búfer circular local que nunca se sube",
    ne: "तपाईंकै उपकरणमा मात्र — कहिल्यै अपलोड नहुने स्थानीय रिङ बफर",
    fr: "Votre propre appareil uniquement — un tampon circulaire local jamais téléversé",
  },
  "priv.tbl.r5.y": {
    en: "Troubleshooting, if you choose to share it",
    ru: "Диагностика — если вы сами решите поделиться",
    fa: "عیب‌یابی، اگر بخواهید آن را به اشتراک بگذارید",
    ar: "استكشاف الأخطاء وإصلاحها، إذا اخترت مشاركته",
    es: "Diagnóstico de problemas, si decide compartirlo",
    ne: "समस्या निवारण, तपाईंले सेयर गर्न चाहेमा",
    fr: "Dépannage, si vous choisissez de le partager",
  },
  "priv.tbl.r5.rt": {
    en: "Local, rotates on your device",
    ru: "Локально, перезаписывается на устройстве",
    fa: "محلی، روی دستگاه شما می‌چرخد",
    ar: "محلي، يتجدد على جهازك",
    es: "Local, rota en su dispositivo",
    ne: "स्थानीय, तपाईंको उपकरणमै घुम्छ",
    fr: "Local, rotation sur votre appareil",
  },
  "priv.tbl.r6.d": {
    en: "Bot session state (only if you use the Telegram bot)",
    ru: "Состояние сессии бота (только если пользуетесь Telegram-ботом)",
    fa: "وضعیت نشست ربات (فقط اگر از ربات Telegram استفاده می‌کنید)",
    ar: "حالة جلسة البوت (فقط إذا كنت تستخدم بوت Telegram)",
    es: "Estado de sesión del bot (solo si usa el bot de Telegram)",
    ne: "बोट सेसन अवस्था (Telegram बोट प्रयोग गर्नुहुन्छ भने मात्र)",
    fr: "État de session du bot (uniquement si vous utilisez le bot Telegram)",
  },
  "priv.tbl.r6.w": {
    en: "Telegram; the cabinet stores account and subscription state",
    ru: "Telegram; в кабинете хранится состояние аккаунта и подписки",
    fa: "Telegram؛ کابینت وضعیت حساب و اشتراک را ذخیره می‌کند",
    ar: "Telegram؛ يخزّن لوحة التحكم حالة الحساب والاشتراك",
    es: "Telegram; el panel guarda el estado de cuenta y suscripción",
    ne: "Telegram; क्याबिनेटले खाता र सदस्यता अवस्था राख्छ",
    fr: "Telegram ; le coffre stocke l\'état du compte et de l\'abonnement",
  },
  "priv.tbl.r6.y": {
    en: "Delivery and support",
    ru: "Доставка и поддержка",
    fa: "تحویل و پشتیبانی",
    ar: "التسليم والدعم",
    es: "Entrega y soporte",
    ne: "वितरण र सहयोग",
    fr: "Livraison et support",
  },
  "priv.tbl.r6.rt": {
    en: "Until deleted",
    ru: "До удаления",
    fa: "تا زمان حذف",
    ar: "حتى الحذف",
    es: "Hasta su eliminación",
    ne: "मेटिन्जेल",
    fr: "Jusqu\'à suppression",
  },
  "priv.tbl.proc.h": {
    en: "Processors involved",
    ru: "Задействованные процессоры",
    fa: "پردازش‌گرهای درگیر",
    ar: "المعالجون المعنيون",
    es: "Encargados de tratamiento",
    ne: "संलग्न प्रोसेसरहरू",
    fr: "Sous-traitants impliqués",
  },
  "priv.tbl.proc.p": {
    en: "Telegram (account delivery and support, telegram.org), certified payment partners for card/crypto processing (named at checkout — we never receive your card details), and the hosting provider that runs our endpoints. A complete, up-to-date processor list is available on request via Telegram.",
    ru: "Telegram (доставка аккаунта и поддержка, telegram.org), сертифицированные платёжные партнёры для оплаты картой/СБП/криптой (указываются при оплате — данные карты нам недоступны) и хостинг-провайдер наших конечных точек. Полный актуальный список процессоров — по запросу в Telegram.",
    fa: "Telegram (تحویل حساب و پشتیبانی، telegram.org)، شرکای پرداخت معتبر برای پردازش کارت/رمزارز (در صفحه پرداخت نام می‌بریم — هرگز جزئیات کارت شما را دریافت نمی‌کنیم) و ارائه‌دهنده هاستینگ که نقاط خروج ما را اجرا می‌کند. فهرست کامل و به‌روز پردازش‌گرها از طریق Telegram در صورت درخواست ارائه می‌شود.",
    ar: "Telegram (تسليم الحسابات والدعم، telegram.org)، وشركاء الدفع المعتمدون لمعالجة البطاقات/العملات المشفرة (يُذكرون عند الدفع — لا نستلم تفاصيل بطاقتك أبدًا)، ومزود الاستضافة الذي يشغّل نقاط الخروج لدينا. القائمة الكاملة والمحدثة لمعالجات البيانات متاحة عند الطلب عبر Telegram.",
    es: "Telegram (entrega de cuentas y soporte, telegram.org), proveedores de pago certificados para el procesamiento de tarjetas/cripto (indicados al pagar — nunca recibimos los datos de su tarjeta) y el proveedor de hosting que ejecuta nuestros puntos de salida. La lista completa y actualizada de procesadores está disponible a petición vía Telegram.",
    ne: "Telegram (खाता वितरण र सहयोग, telegram.org), कार्ड/क्रिप्टो प्रशोधनका लागि प्रमाणित भुक्तानी साझेदारहरू (चेकआउटमा नाम दिइन्छ — तपाईंको कार्ड विवरण हामीले कहिल्यै लिँदैनौं), र हाम्रा निकास चलाउने होस्टिङ प्रदायक। पूर्ण, अद्यावधिक प्रशोधक सूची Telegram मार्फत अनुरोधमा उपलब्ध छ।",
    fr: "Telegram (livraison des comptes et support, telegram.org), partenaires de paiement certifiés pour le traitement carte/crypto (nommés au moment du paiement — nous ne recevons jamais les détails de votre carte) et l\'hébergeur qui exploite nos points de sortie. La liste complète et à jour des sous-traitants est disponible sur demande via Telegram.",
  },
  "priv.tbl.note": {
    en: "This table describes the current architecture; if practices change, this page changes first.",
    ru: "Таблица описывает текущую архитектуру; при изменениях эта страница обновляется первой.",
    fa: "این جدول معماری فعلی را توصیف می‌کند؛ اگر رویه‌ها تغییر کنند، این صفحه اولین جایی است که تغییر می‌کند.",
    ar: "يصف هذا الجدول البنية الحالية؛ إذا تغيرت الممارسات، تتغير هذه الصفحة أولًا.",
    es: "Esta tabla describe la arquitectura actual; si las prácticas cambian, esta página cambia primero.",
    ne: "यो तालिका हालको आर्किटेक्चर देखाउँछ; अभ्यास परिवर्तन भए यो पृष्ठ सबैभन्दा पहिले परिवर्तन हुन्छ।",
    fr: "Ce tableau décrit l\'architecture actuelle ; si les pratiques changent, cette page change d\'abord.",
  },
  "cap.status.h": {
    en: "Capability status",
    ru: "Статус возможностей",
    fa: "وضعیت قابلیت‌ها",
    ar: "حالة القدرات",
    es: "Estado de las funciones",
    ne: "क्षमता स्थिति",
    fr: "État des fonctionnalités",
  },
  "cap.status.tagline": {
    en: "An honest overview of what is live today and what is being built.",
    ru: "Честный обзор того, что уже работает и что в разработке.",
    fa: "مروری صادقانه بر آنچه امروز فعال است و آنچه در حال ساخته‌شدن است.",
    ar: "نظرة صادقة على ما هو مفعّل اليوم وما هو قيد التطوير.",
    es: "Una descripción honesta de lo que ya está activo y de lo que se está construyendo.",
    ne: "आज जे सक्रिय छ र जे निर्माण भइरहेको छ त्यसको ईमानदार अवलोकन।",
    fr: "Un aperçu honnête de ce qui est actif aujourd'hui et de ce qui est en cours de construction.",
  },
  "cap.status.live.h": {
    en: "Available now",
    ru: "Доступно сейчас",
    fa: "هم اکنون موجود",
    ar: "متاح الآن",
    es: "Disponible ahora",
    ne: "अहिले उपलब्ध",
    fr: "Disponible dès maintenant",
  },
  "cap.status.dev.h": {
    en: "In development",
    ru: "В разработке",
    fa: "در حال توسعه",
    ar: "قيد التطوير",
    es: "En desarrollo",
    ne: "विकासमा",
    fr: "En développement",
  },
  "cap.live.1": {
    en: "Android VPN client with one-tap connect",
    ru: "Android-клиент с подключением в одно касание",
    fa: "کلاینت VPN اندروید با اتصال یک‌ضربه‌ای",
    ar: "عميل VPN لأندرويد مع اتصال بلمسة واحدة",
    es: "Cliente VPN para Android con conexión de un toque",
    ne: "एक-ट्याप जडानसँग एन्ड्रोइड VPN क्लाइन्ट",
    fr: "Client VPN Android avec connexion en un geste",
  },
  "cap.live.2": {
    en: "Account-based access and subscription management",
    ru: "Доступ по аккаунту и управление подпиской",
    fa: "دسترسی مبتنی بر حساب و مدیریت اشتراک",
    ar: "وصول قائم على الحساب وإدارة الاشتراكات",
    es: "Acceso basado en cuenta y gestión de suscripción",
    ne: "खाता-आधारिपहुँच र सदस्यता व्यवस्थापन",
    fr: "Accès par compte et gestion des abonnements",
  },
  "cap.live.3": {
    en: "Encrypted VPN connections end to end",
    ru: "Сквозное шифрование VPN-соединений",
    fa: "اتصالات VPN رمزنگاری‌شده از ابتدا تا انتها",
    ar: "اتصالات VPN مشفرة من الطرف إلى الطرف",
    es: "Conexiones VPN cifradas de extremo a extremo",
    ne: "अन्त्य-अन्त इन्क्रिप्सन गरिएका VPN जडानहरू",
    fr: "Connexions VPN chiffrées de bout en bout",
  },
  "cap.live.4": {
    en: "Automatic connection health checks with backup routes",
    ru: "Автоматические проверки соединения и резервные маршруты",
    fa: "بررسی خودکار سلامت اتصال با مسیرهای جایگزین",
    ar: "فحوص صحية تلقائية للاتصال مع مسارات بديلة",
    es: "Comprobaciones automáticas de salud de la conexión con rutas de respaldo",
    ne: "बैकअप रूटहरूसँग स्वचालित जडान स्वास्थ्य जाँच",
    fr: "Contrôles automatiques de santé de la connexion avec routes de secours",
  },
  "cap.dev.1": {
    en: "Expanded route resilience and alternate entry paths",
    ru: "Расширенная устойчивость маршрутов и альтернативные точки входа",
    fa: "تاب‌آوری گسترده‌تر مسیرها و مسیرهای ورود جایگزین",
    ar: "مرونة موسّعة للمسارات ومسارات دخول بديلة",
    es: "Mayor resiliencia de rutas y puntos de entrada alternativos",
    ne: "विस्तारित रूट टिकाउपना र वैकल्पिक प्रवेश मार्गहरू",
    fr: "Résilience des routes élargie et points d'entrée alternatifs",
  },
  "cap.dev.2": {
    en: "IPv4/IPv6 connection selection",
    ru: "Выбор IPv4/IPv6-подключения",
    fa: "انتخاب اتصال IPv4/IPv6",
    ar: "اختيار اتصال IPv4/IPv6",
    es: "Selección de conexión IPv4/IPv6",
    ne: "IPv4/IPv6 जडान चयन",
    fr: "Sélection de connexion IPv4/IPv6",
  },
  "cap.dev.3": {
    en: "Advanced split-routing policies",
    ru: "Продвинутые политики сплит-роутинга",
    fa: "سیاست‌های پیشرفته مسیریابی تقسیمی",
    ar: "سياسات متقدمة للتوجيه المنقسم",
    es: "Políticas avanzadas de enrutamiento dividido",
    ne: "उन्नत विभाजित-रूटिङ नीतिहरू",
    fr: "Politiques avancées de routage divisé",
  },
  "cap.dev.4": {
    en: "Ad Guard network-level filtering (rolling out)",
    ru: "Сетевая фильтрация Ad Guard (выкатывается)",
    fa: "فیلترکردن Ad Guard در سطح شبکه (در حال عرضه)",
    ar: "تصفية Ad Guard على مستوى الشبكة (قيد الطرح)",
    es: "Filtrado Ad Guard a nivel de red (en despliegue)",
    ne: "एड गार्ड नेटवर्क-स्तरीय फिल्टरिङ (रोलिङ आउट)",
    fr: "Filtrage Ad Guard au niveau du réseau (déploiement en cours)",
  },
  "dl.verify.h": {
    en: "Verify before you install",
    ru: "Проверяйте перед установкой",
    fa: "قبل از نصب بررسی کنید",
    ar: "تحقق قبل التثبيت",
    es: "Verifica antes de instalar",
    ne: "इन्स्टल गर्नु अघि जाँच गर्नुहोस्",
    fr: "Vérifiez avant d'installer",
  },
  "dl.meta.none": {
    en: "Version, checksum (SHA-256) and system requirements are published with every release on our GitHub Releases page — check them before installing.",
    ru: "Версия, контрольная сумма (SHA-256) и системные требования публикуются с каждым релизом на нашей странице GitHub Releases — проверьте их перед установкой.",
    fa: "نسخه، چک‌سام (SHA-256) و پیش‌نیازهای سیستم با هر انتشار در صفحه GitHub Releases ما منتشر می‌شود — پیش از نصب بررسی کنید.",
    ar: "تُنشر نسخة الإصدار وبصمة التحقق (SHA-256) ومتطلبات النظام مع كل إصدار على صفحة GitHub Releases لدينا — تحقق منها قبل التثبيت.",
    es: "La versión, el checksum (SHA-256) y los requisitos del sistema se publican con cada versión en nuestra página de GitHub Releases — verifícalos antes de instalar.",
    ne: "संस्करण, चेकसम (SHA-256) र प्रणाली आवश्यकताहरू हामी विकास पृष्ठमा प्रत्येक रिलिजसँग प्रकाशित गरिन्छन् — स्थापना गर्नुअघि तिनीहरू जाँच गर्नुहोस्।",
    fr: "La version, le checksum (SHA-256) et la configuration système requise sont publiés avec chaque version sur notre page GitHub Releases — vérifiez-les avant d'installer.",
  },
  "dl.steps.h": {
    en: "Installation",
    ru: "Установка",
    fa: "نصب",
    ar: "التثبيت",
    es: "Instalación",
    ne: "स्थापना",
    fr: "Installation",
  },
  "dl.step1": {
    en: "Download the APK from our GitHub Releases page — not from third-party mirrors.",
    ru: "Скачайте APK со страницы GitHub Releases — а не со сторонних зеркал.",
    fa: "فایل APK را از صفحه GitHub Releases ما دانلود کنید — نه از آینه‌های شخص ثالث.",
    ar: "نزّل ملف APK من صفحة GitHub Releases لدينا — لا من المرايا الخارجية.",
    es: "Descarga el APK desde nuestra página de GitHub Releases — no desde espejos de terceros.",
    ne: "हाम्रो GitHub रिलिज पृष्ठबाट APK डाउनलोड गर्नुहोस् — तेस्रो-पक्षका मिररहरूबाट होइन।",
    fr: "Téléchargez l'APK depuis notre page GitHub Releases — pas depuis des miroirs tiers.",
  },
  "dl.step2": {
    en: "Verify the SHA-256 checksum matches the value published with the release.",
    ru: "Убедитесь, что SHA-256 совпадает со значением, опубликованным вместе со сборкой.",
    fa: "بررسی کنید چک‌سام SHA-256 با مقدار منتشرشده همراه نسخه یکسان باشد.",
    ar: "تحقق من أن بصمة SHA-256 تطابق القيمة المنشورة مع الإصدار.",
    es: "Verifica que el checksum SHA-256 coincida con el valor publicado con la versión.",
    ne: "SHA-256 चेकसम रिलिजसँग प्रकाशित मानसँग मेल खाने भएको छ छान्नुहोस्।",
    fr: "Vérifiez que le checksum SHA-256 correspond à la valeur publiée avec la version.",
  },
  "dl.step3": {
    en: "Allow installation from this source only for this file.",
    ru: "Разрешите установку из этого источника только для этого файла.",
    fa: "اجازه نصب از این منبع را فقط برای همین فایل بدهید.",
    ar: "اسمح بالتثبيت من هذا المصدر لهذا الملف فقط.",
    es: "Permite la instalación desde esta fuente solo para este archivo.",
    ne: "यो फाइलका लागि मात्र यस स्रोतबाट स्थापना गर्न अनुमति दिनुहोस्।",
    fr: "Autorisez l'installation depuis cette source uniquement pour ce fichier.",
  },
  "dl.step4": {
    en: "Open the app, sign in or create an account, and tap Connect.",
    ru: "Откройте приложение, войдите или создайте аккаунт и нажмите «Подключить».",
    fa: "اپ را باز کنید، وارد شوید یا حساب بسازید و روی «اتصال» بزنید.",
    ar: "افتح التطبيق، وسجّل الدخول أو أنشئ حسابًا، ثم اضغط «اتصال».",
    es: "Abre la app, inicia sesión o crea una cuenta y toca Conectar.",
    ne: "एप खोल्नुहोस्, लग इन गर्नुहोस् वा खाता सिर्जना गर्नुहोस्, र जडान गर्न ट्याप गर्नुहोस्।",
    fr: "Ouvrez l'app, connectez-vous ou créez un compte, puis touchez Se connecter.",
  },
  /* r38: download platform hint */
  "dl.hint.android": {
    en: "You’re on Android — the APK above is exactly what you need.",
    ru: "У вас Android — APK-файл выше — это именно то, что вам нужно.",
    fa: "شما اندروید دارید — فایل APK بالا دقیقاً همان چیزی است که نیاز دارید.",
    ar: "أنت تستخدم أندرويد — ملف APK أعلاه هو بالضبط ما تحتاجه.",
    es: "Estás en Android: el APK de arriba es exactamente lo que necesitas.",
    ne: "तपाईं एन्ड्रोइडमा हुनुहुन्छ — माथिको APK नै तपाईंलाई चाहिने कुरा हो।",
    fr: "Vous êtes sur Android — le fichier APK ci-dessus est exactement ce qu'il vous faut.",
  },
  "dl.hint.other": {
    en: "Not on Android? The app currently ships as an Android APK — for other platforms, ask via the Telegram bot.",
    ru: "У вас не Android? Приложение пока распространяется в виде APK для Android — о других платформах спросите в Telegram-боте.",
    fa: "اندروید ندارید؟ برنامه در حال حاضر به‌صورت APK اندروید ارائه می‌شود — برای سایر پلتفرم‌ها از طریق ربات تلگرام بپرسید.",
    ar: "لا تستخدم أندرويد؟ يُوزَّع التطبيق حاليًا كملف APK لأندرويد — للمنصات الأخرى، اسأل عبر بوت تلغرام.",
    es: "¿No estás en Android? La app por ahora se distribuye como APK de Android; para otras plataformas, consulta en el bot de Telegram.",
    ne: "एन्ड्रोइडमा होइन? एप अहिले एन्ड्रोइड APK का रूपमा उपलब्ध छ — अन्य प्लेटफर्मका लागि टेलिग्राम बोटमार्फत सोध्नुहोस्।",
    fr: "Pas sur Android ? L’application est actuellement distribuée en APK Android — pour les autres plateformes, demandez via le bot Telegram.",
  },
  /* r44: checkout flow localization + remaining a11y labels */
  "price.cta": {
    en: "Get Premium →",
    ru: "Купить Премиум →",
    fa: "دریافت پرمیوم →",
    ar: "اشترك في بريميوم →",
    es: "Conseguir Premium →",
    ne: "प्रिमियम लिनुहोस् →",
    fr: "Obtenir Premium →",
  },
  "checkout.close": { en: "Close checkout", ru: "Закрыть оформление", fa: "بستن پرداخت", ar: "إغلاق الدفع", es: "Cerrar el pago", ne: "चेकआउट बन्द गर्नुहोस्", fr: "Fermer le paiement" },
  "a11y.clear.search": { en: "Clear search", ru: "Очистить поиск", fa: "پاک کردن جستجو", ar: "مسح البحث", es: "Limpiar búsqueda", ne: "खोज खाली गर्नुहोस्", fr: "Effacer la recherche" },
  "a11y.copy.group": { en: "Copy contact details", ru: "Копирование контактных данных", fa: "کپی اطلاعات تماس", ar: "نسخ بيانات الاتصال", es: "Copiar datos de contacto", ne: "सम्पर्क विवरण प्रतिलिपि गर्नुहोस्", fr: "Copier les coordonnées" },
  "a11y.lang.selector": { en: "Language selection", ru: "Выбор языка", fa: "انتخاب زبان", ar: "اختيار اللغة", es: "Selección de idioma", ne: "भाषा छनोट", fr: "Choix de la langue" },
  /* r43: localized theme-toggle aria-labels */
  "theme.light": {
    en: "Switch to light mode",
    ru: "Включить светлую тему",
    fa: "تغییر به حالت روشن",
    ar: "التبديل إلى الوضع الفاتح",
    es: "Cambiar al modo claro",
    ne: "उज्यालो मोडमा जानुहोस्",
    fr: "Passer en mode clair",
  },
  "theme.dark": {
    en: "Switch to dark mode",
    ru: "Включить тёмную тему",
    fa: "تغییر به حالت تاریک",
    ar: "التبديل إلى الوضع الداكن",
    es: "Cambiar al modo oscuro",
    ne: "अँध्यारो मोडमा जानुहोस्",
    fr: "Passer en mode sombre",
  },
  /* r40: public-repo secondary CTA + localized footer releases link */
  "dl.hero.source": {
    en: "Browse the source code",
    ru: "Исходный код",
    fa: "مشاهده کد منبع",
    ar: "تصفّح الكود المصدري",
    es: "Ver el código fuente",
    ne: "सोर्स कोड हेर्नुहोस्",
    fr: "Voir le code source",
  },
  /* r45: PWA install affordance (beforeinstallprompt on download page) */
  "dl.install": {
    en: "Install the app",
    ru: "Установить приложение",
    fa: "نصب برنامه",
    ar: "تثبيت التطبيق",
    es: "Instalar la aplicación",
    ne: "एप इन्स्टल गर्नुहोस्",
    fr: "Installer l’application",
  },
  "footer.releases": {
    en: "GitHub Releases",
    ru: "Релизы на GitHub",
    fa: "نسخه‌های گیت‌هاب",
    ar: "إصدارات GitHub",
    es: "Lanzamientos de GitHub",
    ne: "GitHub रिलिजहरू",
    fr: "Versions GitHub",
  },
  /* r38: localized release-meta grid labels (SHA-256 stays universal) */
  "dl.meta.version": { en: "Version", ru: "Версия", fa: "نسخه", ar: "الإصدار", es: "Versión", ne: "संस्करण", fr: "Version" },
  "dl.meta.released": { en: "Released", ru: "Дата выпуска", fa: "تاریخ انتشار", ar: "تاريخ الإصدار", es: "Fecha de lanzamiento", ne: "जारी मिति", fr: "Date de sortie" },
  "dl.meta.package": { en: "Package", ru: "Пакет", fa: "بسته", ar: "الحزمة", es: "Paquete", ne: "प्याकेज", fr: "Paquet" },
  "dl.meta.size": { en: "Size", ru: "Размер", fa: "حجم", ar: "الحجم", es: "Tamaño", ne: "आकार", fr: "Taille" },
  "dl.meta.minandroid": { en: "Minimum Android", ru: "Мин. Android", fa: "حداقل اندروید", ar: "الحد الأدنى لأندرويد", es: "Android mínimo", ne: "न्यूनतम एन्ड्रोइड", fr: "Android minimum" },
  "dl.meta.status": { en: "Status", ru: "Статус", fa: "وضعیت", ar: "الحالة", es: "Estado", ne: "स्थिति", fr: "Statut" },
  /* r112: the fetch-landed status VALUE was hardcoded EN "Stable" while every
     label around it localized — the one cell that stayed English on a RU/FA
     page once a release ships. */
  "dl.meta.stable": { en: "Stable", ru: "Стабильный", fa: "پایدار", ar: "مستقر", es: "Estable", ne: "स्थिर", fr: "Stable" },

  /* r134: QR phone-transfer card (download.html) — desktop users scan the
     code to continue on the phone where the APK installs. URL encoded is the
     page's rel=canonical (r63 pattern), so locale/query variants all encode
     the one primary URL. */
  "dl.qr.title": {
    en: "Open on your phone",
    ru: "Откройте на телефоне",
    fa: "روی گوشی خود باز کنید",
    ar: "افتحها على هاتفك",
    es: "Ábrelo en tu teléfono",
    ne: "तपाईंको फोनमा खोल्नुहोस्",
    fr: "Ouvrez-le sur votre téléphone",
  },
  "dl.qr.sub": {
    en: "Point your camera at the code — the download page opens on your phone.",
    ru: "Наведите камеру на код — страница загрузки откроется на телефоне.",
    fa: "دوربین را روی کد بگیرید — صفحه دانلود روی گوشی‌تان باز می‌شود.",
    ar: "وجّه الكاميرا نحو الرمز — تُفتح صفحة التحميل على هاتفك.",
    es: "Apunta la cámara al código: la página de descarga se abre en tu teléfono.",
    ne: "कोडमा क्यामेरा तेर्साउनुहोस् — डाउनलोड पृष्ठ तपाईंको फोनमा खुल्छ।",
    fr: "Visez le code avec l’appareil photo — la page de téléchargement s’ouvre sur votre téléphone.",
  },
  "dl.qr.alt": {
    en: "QR code linking to the download page",
    ru: "QR-код со ссылкой на страницу загрузки",
    fa: "کد QR با پیوند به صفحه دانلود",
    ar: "رمز QR يحيل إلى صفحة التحميل",
    es: "Código QR con enlace a la página de descarga",
    ne: "डाउनलोड पृष्ठमा लिङ्क गर्ने QR कोड",
    fr: "Code QR pointant vers la page de téléchargement",
  },
  /* r134: "Save as PDF" chip on the legal trio — the print styles are
     verified on real paper (r133), so give visitors a one-tap path to them. */
  "legal.print": {
    en: "Save as PDF",
    ru: "Сохранить в PDF",
    fa: "ذخیره به‌صورت PDF",
    ar: "حفظ بصيغة PDF",
    es: "Guardar en PDF",
    ne: "PDF का रूपमा सुरक्षित गर्नुहोस्",
    fr: "Enregistrer en PDF",
  },
  /* r42: FAQ permalink anchor */
  "faq.anchor.label": {
    en: "Copy link to this answer",
    ru: "Скопировать ссылку на этот ответ",
    fa: "کپی پیوند به این پاسخ",
    ar: "نسخ رابط هذه الإجابة",
    es: "Copiar enlace a esta respuesta",
    ne: "यो उत्तरको लिङ्क प्रतिलिपि गर्नुहोस्",
    fr: "Copier le lien vers cette réponse",
  },
  /* r76 — the same '#' permalink anchor on privacy/terms/refund, where the
     block is a policy clause; section 7b switches aria/title by pathname. */
  "faq.anchor.clause": {
    en: "Copy link to this clause",
    ru: "Скопировать ссылку на этот пункт",
    fa: "کپی پیوند به این بند",
    ar: "نسخ رابط هذا البند",
    es: "Copiar enlace a esta cláusula",
    ne: "यो धाराको लिङ्क प्रतिलिपि गर्नुहोस्",
    fr: "Copier le lien vers cette clause",
  },
  /* r110 — the same '#' permalink anchor on how-it-works, where the h2 is a
     narrative step ("Install the app", "Tap Connect"); section 7c names the
     chip for the step so support can deep-link straight to one stage. */
  "faq.anchor.step": {
    en: "Copy link to this step",
    ru: "Скопировать ссылку на этот шаг",
    fa: "کپی پیوند به این مرحله",
    ar: "نسخ رابط هذه الخطوة",
    es: "Copiar enlace a este paso",
    ne: "यो चरणको लिङ्क प्रतिलिपि गर्नुहोस्",
    fr: "Copier le lien vers cette étape",
  },
  "faq.filter.label": {
    en: "Search questions",
    ru: "Поиск по вопросам",
    fa: "جست‌وجوی پرسش‌ها",
    ar: "البحث في الأسئلة",
    es: "Buscar preguntas",
    ne: "प्रश्न खोज्नुहोस्",
    fr: "Rechercher parmi les questions",
  },
  "faq.filter.placeholder": {
    en: "Type to filter…",
    ru: "Введите для фильтрации…",
    fa: "برای پالایش تایپ کنید…",
    ar: "اكتب للتصفية…",
    es: "Escribe para filtrar…",
    ne: "फिल्टर गर्न टाइप गर्नुहोस्…",
    fr: "Tapez pour filtrer…",
  },
  "faq.filter.clear": {
    en: "Clear search",
    ru: "Очистить поиск",
    fa: "پاک کردن جست‌وجو",
    ar: "مسح البحث",
    es: "Borrar la búsqueda",
    ne: "खोज खाली गर्नुहोस्",
    fr: "Effacer la recherche",
  },
  "faq.filter.results": {
    en: "{n} of {total} questions match",
    ru: "Найдено вопросов: {n} из {total}",
    fa: "{n} پرسش از {total} پرسش مطابقت دارد",
    ar: "{n} من أصل {total} سؤالًا مطابقًا",
    es: "{n} de {total} preguntas coinciden",
    ne: "{total} मध्ये {n} प्रश्न मिले",
    fr: "{n} questions sur {total} correspondent",
  },
  /* r100: shown in the status line when a language switch resets a text
     query (keywords are locale-bound — an EN term re-applied to RU text is a
     guaranteed dead end). Categories survive: data-cat is locale-independent. */
  "faq.filter.cleared": {
    en: "Search reset for the new language.",
    ru: "Поиск сброшен для нового языка.",
    fa: "جست‌وجو برای زبان جدید بازنشانی شد.",
    ar: "تمت إعادة تعيين البحث للغة الجديدة.",
    es: "Búsqueda reiniciada para el nuevo idioma.",
    ne: "नयाँ भाषाका लागि खोज पुनःसेट गरियो।",
    fr: "Recherche réinitialisée pour la nouvelle langue.",
  },
  /* r56: FAQ no-results empty state (shown when a query/category matches 0 items) */
  "faq.empty.title": {
    en: "No matching questions",
    ru: "Ничего не найдено",
    fa: "سوالی یافت نشد",
    ar: "لا توجد أسئلة مطابقة",
    es: "No hay preguntas coincidentes",
    ne: "कुनै मिल्ने प्रश्न भेटिएन",
    fr: "Aucune question correspondante",
  },
  "faq.empty.sub": {
    en: "Try different keywords or reset the filters.",
    ru: "Попробуйте изменить запрос или сбросить фильтры.",
    fa: "کلیدواژه‌های دیگری امتحان کنید یا فیلترها را بازنشانی کنید.",
    ar: "جرّب كلمات مفتاحية أخرى أو أعد تعيين عوامل التصفية.",
    es: "Prueba con otras palabras o restablece los filtros.",
    ne: "अर्को शब्द प्रयोग गर्नुहोस् वा फिल्टरहरू रिसेट गर्नुहोस्।",
    fr: "Essayez d’autres mots-clés ou réinitialisez les filtres.",
  },
  "faq.empty.reset": {
    en: "Reset filters",
    ru: "Сбросить фильтры",
    fa: "بازنشانی فیلترها",
    ar: "إعادة تعيين عوامل التصفية",
    es: "Restablecer filtros",
    ne: "फिल्टरहरू रिसेट गर्नुहोस्",
    fr: "Réinitialiser les filtres",
  },
  "faq.filter.hint": {
    en: "Press the slash key to jump to search",
    ru: "Нажмите клавишу «/», чтобы перейти к поиску",
    fa: "برای پرش به جست‌وجو کلید / را فشار دهید",
    ar: "اضغط مفتاح / للانتقال إلى البحث",
    es: "Pulsa la tecla / para ir a la búsqueda",
    ne: "खोजमा जानका लागि / कुञ्जी थिच्नुहोस्",
    fr: "Appuyez sur la touche / pour accéder à la recherche",
  },
  "cap.verified": {
    en: "Routes last verified:",
    ru: "Маршруты проверены:",
    fa: "آخرین بررسی مسیرها:",
    ar: "آخر تحقّق من المسارات:",
    es: "Rutas verificadas por última vez:",
    ne: "मार्गहरू अन्तिम पटक जाँचिएको:",
    fr: "Dernière vérification des routes :",
  },
  "a11y.backtop": {
    en: "Back to top",
    ru: "Наверх",
    fa: "بازگشت به بالا",
    ar: "العودة إلى الأعلى",
    es: "Volver arriba",
    ne: "माथि फर्कनुहोस्",
    fr: "Retour en haut",
  },
  "a11y.tbl.features": {
    en: "Features comparison table",
    ru: "Таблица сравнения возможностей",
    fa: "جدول مقایسه امکانات",
    ar: "جدول مقارنة الميزات",
    es: "Tabla comparativa de funciones",
    ne: "विशेषता तुलना तालिका",
    fr: "Tableau comparatif des fonctionnalités",
  },
  "a11y.tbl.comparison": {
    en: "VPN comparison matrix",
    ru: "Матрица сравнения VPN",
    fa: "ماتریس مقایسه VPN",
    ar: "مصفوفة مقارنة VPN",
    es: "Matriz comparativa de VPN",
    ne: "VPN तुलना म्याट्रिक्स",
    fr: "Matrice de comparaison VPN",
  },
  "a11y.tbl.privacy": {
    en: "Data visibility table",
    ru: "Таблица видимости данных",
    fa: "جدول نمایش داده‌ها",
    ar: "جدول رؤية البيانات",
    es: "Tabla de visibilidad de datos",
    ne: "डाटा दृश्यता तालिका",
    fr: "Tableau de visibilité des données",
  },
  "a11y.copy.email": {
    en: "Copy support e-mail address",
    ru: "Скопировать адрес почты поддержки",
    fa: "کپی نشانی ایمیل پشتیبانی",
    ar: "انسخ عنوان البريد الإلكتروني للدعم",
    es: "Copiar la dirección de correo de soporte",
    ne: "सहयोग इमेल ठेगाना प्रतिलिपि गर्नुहोस्",
    fr: "Copier l'adresse e-mail du support",
  },
  /* r77 — icon-only chip next to the Payment ID on success.html (appears
     only when ?payment_id= is present; refund/support chats ask for it). */
  "a11y.copy.payment": {
    en: "Copy payment ID",
    ru: "Скопировать ID платежа",
    fa: "کپی شناسه پرداخت",
    ar: "انسخ معرّف الدفع",
    es: "Copiar el ID de pago",
    ne: "भुक्तानी आईडी प्रतिलिपि गर्नुहोस्",
    fr: "Copier l'identifiant de paiement",
  },
  "a11y.copy.tg": {
    en: "Copy Telegram handle",
    ru: "Скопировать ник в Telegram",
    fa: "کپی آیدی تلگرام",
    ar: "انسخ معرّف تيليجرام",
    es: "Copiar el usuario de Telegram",
    ne: "टेलिग्राम ह्यान्डल प्रतिलिपि गर्नुहोस्",
    fr: "Copier l'identifiant Telegram",
  },
  /* r47: post-payment success page — full localization of the conversion
     funnel's final step (was hardcoded EN incl. the JS plan-name map) */
  "success.h1": {
    en: "Payment Successful!",
    ru: "Оплата прошла успешно!",
    fa: "پرداخت با موفقیت انجام شد!",
    ar: "تم الدفع بنجاح!",
    es: "¡Pago completado con éxito!",
    ne: "भुक्तानी सफल भयो!",
    fr: "Paiement réussi !",
  },
  "success.sub": {
    en: "Your premium access is now active.",
    ru: "Ваш премиум-доступ уже активен.",
    fa: "دسترسی پرمیوم شما اکنون فعال است.",
    ar: "وصولك المميز مُفعّل الآن.",
    es: "Tu acceso premium ya está activo.",
    ne: "तपाईंको प्रिमियम पहुँच अहिले सक्रिय छ।",
    fr: "Votre accès premium est désormais actif.",
  },
  "success.plan.label": {
    en: "Plan", ru: "Тариф", fa: "طرح", ar: "الخطة", es: "Plan", ne: "योजना", fr: "Formule",
  },
  "success.status.label": {
    en: "Status", ru: "Статус", fa: "وضعیت", ar: "الحالة", es: "Estado", ne: "स्थिति", fr: "Statut",
  },
  "success.active": {
    en: "Active", ru: "Активен", fa: "فعال", ar: "مُفعّل", es: "Activo", ne: "सक्रिय", fr: "Actif",
  },
  "success.payment.label": {
    en: "Payment ID", ru: "ID платежа", fa: "شناسه پرداخت", ar: "معرّف الدفع", es: "ID de pago", ne: "भुक्तानी आईडी", fr: "ID de paiement",
  },
  "success.back.pricing": {
    en: "Back to Pricing",
    ru: "Вернуться к тарифам",
    fa: "بازگشت به تعرفه‌ها",
    ar: "العودة إلى الأسعار",
    es: "Volver a precios",
    ne: "मूल्यमा फर्कनुहोस्",
    fr: "Retour aux tarifs",
  },
  "success.note.app": {
    en: "Open the NullVPN app and log in to activate your premium subscription. If you already have the app, your premium will activate automatically on next launch.",
    ru: "Откройте приложение NullVPN и войдите в аккаунт, чтобы активировать премиум-подписку. Если приложение уже установлено, премиум активируется автоматически при следующем запуске.",
    fa: "برنامه NullVPN را باز کنید و وارد شوید تا اشتراک پرمیوم شما فعال شود. اگر برنامه را از قبل دارید، پرمیوم در اجرای بعدی به‌طور خودکار فعال می‌شود.",
    ar: "افتح تطبيق NullVPN وسجّل الدخول لتفعيل اشتراكك المميز. إذا كان التطبيق مثبّتًا لديك مسبقًا، سيُفعّل المميز تلقائيًا عند التشغيل التالي.",
    es: "Abre la aplicación NullVPN e inicia sesión para activar tu suscripción premium. Si ya tienes la app, tu premium se activará automáticamente en el próximo inicio.",
    ne: "प्रिमियम सदस्यता सक्रिय गर्न NullVPN एप खोल्नुहोस् र लगइन गर्नुहोस्। यदि एप पहिले नै छ भने, अर्को पटक खोल्दा प्रिमियम स्वतः सक्रिय हुनेछ।",
    fr: "Ouvrez l’application NullVPN et connectez-vous pour activer votre abonnement premium. Si l’app est déjà installée, le premium s’activera automatiquement au prochain lancement.",
  },
  "success.note.help": {
    en: "Need help? Telegram <a href='https://t.me/nullvpn_net' target='_blank' rel='noopener'>@nullvpn_net</a> · <a href='mailto:support@nullvpn.net'>support@nullvpn.net</a>",
    ru: "Нужна помощь? Telegram <a href='https://t.me/nullvpn_net' target='_blank' rel='noopener'>@nullvpn_net</a> · <a href='mailto:support@nullvpn.net'>support@nullvpn.net</a>",
    fa: "به کمک نیاز دارید؟ تلگرام <a href='https://t.me/nullvpn_net' target='_blank' rel='noopener'>@nullvpn_net</a> · <a href='mailto:support@nullvpn.net'>support@nullvpn.net</a>",
    ar: "تحتاج مساعدة؟ تيليجرام <a href='https://t.me/nullvpn_net' target='_blank' rel='noopener'>@nullvpn_net</a> · <a href='mailto:support@nullvpn.net'>support@nullvpn.net</a>",
    es: "¿Necesitas ayuda? Telegram <a href='https://t.me/nullvpn_net' target='_blank' rel='noopener'>@nullvpn_net</a> · <a href='mailto:support@nullvpn.net'>support@nullvpn.net</a>",
    ne: "सहयोग चाहियो? टेलिग्राम <a href='https://t.me/nullvpn_net' target='_blank' rel='noopener'>@nullvpn_net</a> · <a href='mailto:support@nullvpn.net'>support@nullvpn.net</a>",
    fr: "Besoin d’aide ? Telegram <a href='https://t.me/nullvpn_net' target='_blank' rel='noopener'>@nullvpn_net</a> · <a href='mailto:support@nullvpn.net'>support@nullvpn.net</a>",
  },
  "success.plan.monthly": {
    en: "Monthly (30 days)", ru: "Месячный (30 дней)", fa: "ماهانه (30 روز)", ar: "شهري (30 يومًا)", es: "Mensual (30 días)", ne: "मासिक (30 दिन)", fr: "Mensuel (30 jours)",
  },
  "success.plan.quarterly": {
    en: "Quarterly (90 days)", ru: "На квартал (90 дней)", fa: "سه‌ماهه (90 روز)", ar: "ربع سنوي (90 يومًا)", es: "Trimestral (90 días)", ne: "त्रैमासिक (90 दिन)", fr: "Trimestriel (90 jours)",
  },
  "success.plan.annual": {
    en: "Annual (365 days)", ru: "Годовой (365 дней)", fa: "سالانه (365 روز)", ar: "سنوي (365 يومًا)", es: "Anual (365 días)", ne: "वार्षिक (365 दिन)", fr: "Annuel (365 jours)",
  },
  "a11y.copied": {
    en: "Copied to clipboard ✓",
    ru: "Скопировано в буфер обмена ✓",
    fa: "در کلیپ‌بورد کپی شد ✓",
    ar: "تم النسخ إلى الحافظة ✓",
    es: "Copiado al portapapeles ✓",
    ne: "क्लिपबोर्डमा प्रतिलिपि भयो ✓",
    fr: "Copié dans le presse-papiers ✓",
  },
  "a11y.copyfail": {
    en: "Could not copy — please copy manually",
    ru: "Не удалось скопировать — скопируйте вручную",
    fa: "کپی نشد — لطفاً به‌صورت دستی کپی کنید",
    ar: "تعذّر النسخ — يُرجى النسخ يدويًا",
    es: "No se pudo copiar; cópialo manualmente",
    ne: "प्रतिलिपि गर्न सकिएन — म्यानुअल रूपमा प्रतिलिपि गर्नुहोस्",
    fr: "Impossible de copier — veuillez copier manuellement",
  },
  "share.btn": {
    en: "Share",
    ru: "Поделиться",
    fa: "هم‌رسانی",
    ar: "مشاركة",
    es: "Compartir",
    ne: "सेयर गर्नुहोस्",
    fr: "Partager",
  },
  "share.text": {
    en: "NullVPN — private internet that works on any network.",
    ru: "NullVPN — приватный интернет, который работает в любой сети.",
    fa: "NullVPN — اینترنتی خصوصی که در هر شبکه‌ای کار می‌کند.",
    ar: "NullVPN — إنترنت خاص يعمل على أي شبكة.",
    es: "NullVPN — internet privado que funciona en cualquier red.",
    ne: "NullVPN — कुनै पनि नेटवर्कमा काम गर्ने निजी इन्टरनेट।",
    fr: "NullVPN — un internet privé qui fonctionne sur n'importe quel réseau.",
  },
  "share.done": {
    en: "Shared — thank you!",
    ru: "Поделились — спасибо!",
    fa: "هم‌رسانی شد — سپاسگزاریم!",
    ar: "تمت المشاركة — شكرًا لك!",
    es: "Compartido — ¡gracias!",
    ne: "सेयर भयो — धन्यवाद!",
    fr: "Partagé — merci !",
  },
  /* r65 — accessible name for the per-answer share chip on the FAQ page
     (icon-only button; the visible context is the answer itself). */
  "share.answer": {
    en: "Share this answer",
    ru: "Поделиться этим ответом",
    fa: "هم‌رسانی این پاسخ",
    ar: "مشاركة هذه الإجابة",
    es: "Compartir esta respuesta",
    ne: "यो उत्तर सेयर गर्नुहोस्",
    fr: "Partager cette réponse",
  },
  /* r76 — same chip on the legal pages (privacy/terms/refund), where the
     .faq-item blocks are clauses of a policy, not answers to questions.
     Section 7b picks this over share.answer by pathname so screen readers
     and hover tooltips name the chip correctly in context. */
  "share.clause": {
    en: "Share this clause",
    ru: "Поделиться этим пунктом",
    fa: "هم‌رسانی این بند",
    ar: "مشاركة هذا البند",
    es: "Compartir esta cláusula",
    ne: "यो धारा सेयर गर्नुहोस्",
    fr: "Partager cette clause",
  },
  /* r66 — accessible name for the per-column share chip in the comparison
     table header (icon-only button; the column itself is the context). */
  "comp.share.col": {
    en: "Share this column",
    ru: "Поделиться этим столбцом",
    fa: "هم‌رسانی این ستون",
    ar: "مشاركة هذا العمود",
    es: "Compartir esta columna",
    ne: "यो स्तम्भ सेयर गर्नुहोस्",
    fr: "Partager cette colonne",
  },
  /* r88 — visible caption for the comparison matrix: the <caption> element is
     the proper HTML way to name a data table (screen readers announce it on
     table entry, complementing the r85 region aria-label). Copy is
     number-free so it never drifts when rows/columns change. */
  "comp.table.caption": {
    en: "Feature matrix — identical criteria checked for every service.",
    ru: "Матрица функций — одни и те же критерии проверены для каждого сервиса.",
    fa: "ماتریس امکانات — معیارهای یکسان برای هر سرویس بررسی شده است.",
    ar: "مصفوفة الميزات — المعايير نفسها تم التحقق منها لكل خدمة.",
    es: "Matriz de funciones — los mismos criterios verificados para cada servicio.",
    ne: "सुविधा म्याट्रिक्स — हरेक सेवाका लागि सोही मापदण्डहरू जाँच गरिएका।",
    fr: "Matrice des fonctionnalités — les mêmes critères vérifiés pour chaque service.",
  },
  /* r67 — verdict legend above the comparison table: names the three status
     colours so the matrix reads correctly at a glance (swatches carry the
     exact .yes/.partial/.no colours, incl. dark-theme variants). */
  "comp.legend.yes": {
    en: "Works as claimed",
    ru: "Работает, как заявлено",
    fa: "همان‌طور که ادعا شده کار می‌کند",
    ar: "يعمل كما هو معلن",
    es: "Funciona como lo anuncian",
    ne: "दाबीअनुसारै काम गर्छ",
    fr: "Fonctionne comme annoncé",
  },
  "comp.legend.partial": {
    en: "Partially",
    ru: "Частично",
    fa: "تاحدودی",
    ar: "جزئيًا",
    es: "Parcialmente",
    ne: "आंशिक रूपमा",
    fr: "Partiellement",
  },
  "comp.legend.no": {
    en: "Does not deliver",
    ru: "Не справляется",
    fa: "برآورده نمی‌شود",
    ar: "لا يفي بوعده",
    es: "No cumple",
    ne: "पूरा गर्दैन",
    fr: "Ne tient pas ses promesses",
  },
  /* r68 — accessible name for the row permalink anchor in the comparison
     table's label column (mirrors faq.anchor.label vocabulary). */
  "comp.anchor.row": {
    en: "Copy link to this row",
    ru: "Скопировать ссылку на эту строку",
    fa: "کپی پیوند به این ردیف",
    ar: "نسخ رابط هذا الصف",
    es: "Copiar enlace a esta fila",
    ne: "यो पङ्क्तिको लिङ्क प्रतिलिपि गर्नुहोस्",
    fr: "Copier le lien vers cette ligne",
  },
  "pricing.anchor.plan": {
    en: "Copy link to this plan",
    ru: "Скопировать ссылку на этот тариф",
    fa: "کپی پیوند به این پلن",
    ar: "نسخ رابط هذه الخطة",
    es: "Copiar enlace a este plan",
    ne: "यो प्लानको लिङ्क प्रतिलिपि गर्नुहोस्",
    fr: "Copier le lien vers cette offre",
  },
  "feat.anchor.row": {
    en: "Copy link to this feature",
    ru: "Скопировать ссылку на эту возможность",
    fa: "کپی پیوند به این ویژگی",
    ar: "نسخ رابط هذه الميزة",
    es: "Copiar enlace a esta característica",
    ne: "यो सुविधाको लिङ्क प्रतिलिपि गर्नुहोस्",
    fr: "Copier le lien vers cette caractéristique",
  },
  /* r69 — offline.html inventory + reconnect (engine section 15). */
  "offline.available": {
    en: "Available offline",
    ru: "Доступно офлайн",
    fa: "به‌صورت آفلاین در دسترس",
    ar: "متاح دون اتصال",
    es: "Disponible sin conexión",
    ne: "अफलाइनमा उपलब्ध",
    fr: "Disponible hors ligne",
  },
  "offline.backonline": {
    en: "Back online — reconnecting…",
    ru: "Соединение восстановлено — перезагружаем…",
    fa: "اتصال برقرار شد — در حال بارگذاری مجدد…",
    ar: "عاد الاتصال — جارٍ إعادة التحميل…",
    es: "Conexión restablecida — recargando…",
    ne: "इन्टरनेट फर्कियो — पुनः लोड हुँदै…",
    fr: "De nouveau en ligne — rechargement…",
  },
  /* r73 — visible label of the comparison text-export chip (section 14
     builds a chat-pasteable summary of the matrix from the live DOM). */
  "comp.copy.text": {
    en: "Copy as text",
    ru: "Копировать как текст",
    fa: "کپی به‌صورت متن",
    ar: "نسخ كنص",
    es: "Copiar como texto",
    ne: "पाठको रूपमा प्रतिलिपि गर्नुहोस्",
    fr: "Copier en tant que texte",
  },
  /* r74 — web3.html bridge controls: share/save the censorship-proof mirror
     URL (delegated share engine, data-share-url override) and a cancel for
     the 1500ms auto-redirect. */
  "web3.share.mirror": {
    en: "Share mirror link",
    ru: "Поделиться ссылкой на зеркало",
    fa: "هم‌رسانی پیوند آینه",
    ar: "مشاركة رابط المرآة",
    es: "Compartir enlace del espejo",
    ne: "मिरर लिङ्क सेयर गर्नुहोस्",
    fr: "Partager le lien miroir",
  },
  "web3.cancel": {
    en: "Stay here",
    ru: "Остаться здесь",
    fa: "اینجا بمان",
    ar: "ابقَ هنا",
    es: "Quedarme aquí",
    ne: "यहीं रहनुहोस्",
    fr: "Rester ici",
  },
  "web3.cancelled": {
    en: "Redirect cancelled — the mirror link stays above.",
    ru: "Переадресация отменена — ссылка на зеркало выше.",
    fa: "هدایت لغو شد — پیوند آینه بالا است.",
    ar: "تم إلغاء التحويل — رابط المرآة بالأعلى.",
    es: "Redirección cancelada — el enlace del espejo queda arriba.",
    ne: "रिडाइरेक्ट रद्द भयो — मिरर लिङ्क माथि छ।",
    fr: "Redirection annulée — le lien miroir reste ci-dessus.",
  },
  "a11y.skip": {
    en: "Skip to main content",
    ru: "Перейти к основному содержимому",
    fa: "پرش به محتوای اصلی",
    ar: "الانتقال إلى المحتوى الرئيسي",
    es: "Saltar al contenido principal",
    ne: "मुख्य सामग्रीमा जानुहोस्",
    fr: "Aller au contenu principal",
  },
  /* 404 page — r37 */
  "nf.title": {
    en: "Page not found",
    ru: "Страница не найдена",
    fa: "صفحه پیدا نشد",
    ar: "الصفحة غير موجودة",
    es: "Página no encontrada",
    ne: "पृष्ठ भेटिएन",
    fr: "Page introuvable",
  },
  /* offline fallback page — r55 (served by sw.js for navigations that fail offline) */
  "offline.title": {
    en: "You’re offline",
    ru: "Вы офлайн",
    fa: "شما آفلاین هستید",
    ar: "أنت غير متصل",
    es: "Sin conexión",
    ne: "तपाईं अफलाइन हुनुहुन्छ",
    fr: "Vous êtes hors ligne",
  },
  "offline.sub": {
    en: "The connection dropped. Pages you already visited may still be available.",
    ru: "Соединение прервалось. Страницы, которые вы уже открывали, могут быть доступны.",
    fa: "اتصال قطع شد. صفحه‌هایی که قبلاً باز کرده‌اید ممکن است همچنان در دسترس باشند.",
    ar: "انقطع الاتصال. الصفحات التي فتحتها مسبقًا قد تبقى متاحة.",
    es: "Se perdió la conexión. Las páginas que ya visitaste pueden seguir estando disponibles.",
    ne: "जडान विच्छेद भयो। तपाईंले पहिले खोलेका पृष्ठहरू अझै उपलब्ध हुन सक्छन्।",
    fr: "La connexion a été perdue. Les pages déjà visitées peuvent rester disponibles.",
  },
  "offline.retry": {
    en: "Try again",
    ru: "Попробовать снова",
    fa: "تلاش دوباره",
    ar: "أعد المحاولة",
    es: "Reintentar",
    ne: "फेरि प्रयास गर्नुहोस्",
    fr: "Réessayer",
  },
  "nf.sub": {
    en: "The page you’re looking for doesn’t exist or has moved.",
    ru: "Запрошенная страница не существует или была перемещена.",
    fa: "صفحه‌ای که دنبالش بودید وجود ندارد یا جابه‌جا شده است.",
    ar: "الصفحة التي تبحث عنها غير موجودة أو تم نقلها.",
    es: "La página que buscas no existe o se ha movido.",
    ne: "तपाईंले खोज्नुभएको पृष्ठ अवस्थित छैन वा सारिएको छ।",
    fr: "La page que vous cherchez n’existe pas ou a été déplacée.",
  },
  "nf.suggest": {
    en: "Did you mean:",
    ru: "Возможно, вы искали:",
    fa: "آیا منظورتان این بود:",
    ar: "هل تقصد:",
    es: "¿Quisiste decir:",
    ne: "तपाईं यसो खोज्नुभएको हो कि:",
    fr: "Vouliez-vous dire :",
  },
  /* r105: 404 FAQ-search recovery form (placeholder doubles as the input's
     aria-label via data-i18n-aria on the same element). */
  "nf.search.ph": {
    en: "Search the FAQ…",
    ru: "Поиск по FAQ…",
    fa: "جستجو در پرسش‌های متداول…",
    ar: "ابحث في الأسئلة الشائعة…",
    es: "Buscar en las preguntas frecuentes…",
    ne: "FAQ मा खोज्नुहोस्…",
    fr: "Rechercher dans la FAQ…",
  },
  "nf.search.go": {
    en: "Search",
    ru: "Найти",
    fa: "جستجو",
    ar: "بحث",
    es: "Buscar",
    ne: "खोज्नुहोस्",
    fr: "Rechercher",
  },
  "dl.hero.h": {
    en: "Download NullVPN",
    ru: "Скачать NullVPN",
    fa: "دانلود NullVPN",
    ar: "حمّل NullVPN",
    es: "Descarga NullVPN",
    ne: "NullVPN डाउनलोड गर्नुहोस्",
    fr: "Téléchargez NullVPN",
  },
  "dl.hero.p": {
    en: "Get the official Android app from our GitHub Releases page — every build ships with its checksum.",
    ru: "Скачайте официальное Android-приложение на нашей странице GitHub Releases — каждая сборка публикуется с контрольной суммой.",
    fa: "برنامهٔ رسمی اندروید را از صفحهٔ GitHub Releases ما دریافت کنید — هر نسخه همراه با چک‌سام منتشر می‌شود.",
    ar: "احصل على تطبيق أندرويد الرسمي من صفحة GitHub Releases لدينا — كل إصدار يُنشر مع بصمة تحقق.",
    es: "Consigue la app oficial de Android en nuestra página de GitHub Releases — cada versión se publica con su checksum.",
    ne: "हाम्रो GitHub Releases पृष्ठबाट आधिकारिक एन्ड्रोइड एप प्राप्त गर्नुहोस् — प्रत्येक बिल्ड चेकसमसहित प्रकाशित हुन्छ।",
    fr: "Obtenez l'application Android officielle depuis notre page GitHub Releases — chaque version est publiée avec sa somme de contrôle.",
  },
  "dl.hero.note": {
    en: "Locked out of GitHub? Reach support via <a href=\"https://t.me/nullvpn_net\" target=\"_blank\" rel=\"noopener\" referrerpolicy=\"no-referrer\">@nullvpn_net</a> or <a href=\"mailto:support@nullvpn.net\">support@nullvpn.net</a>.",
    ru: "GitHub недоступен? Напишите в поддержку — <a href=\"https://t.me/nullvpn_net\" target=\"_blank\" rel=\"noopener\" referrerpolicy=\"no-referrer\">@nullvpn_net</a> или <a href=\"mailto:support@nullvpn.net\">support@nullvpn.net</a>.",
    fa: "به GitHub دسترسی ندارید؟ با پشتیبانی در تماس باشید — <a href=\"https://t.me/nullvpn_net\" target=\"_blank\" rel=\"noopener\" referrerpolicy=\"no-referrer\">@nullvpn_net</a> یا <a href=\"mailto:support@nullvpn.net\">support@nullvpn.net</a>.",
    ar: "لا تستطيع الوصول إلى GitHub؟ تواصل مع الدعم عبر <a href=\"https://t.me/nullvpn_net\" target=\"_blank\" rel=\"noopener\" referrerpolicy=\"no-referrer\">@nullvpn_net</a> أو <a href=\"mailto:support@nullvpn.net\">support@nullvpn.net</a>.",
    es: "¿Sin acceso a GitHub? Contacta con soporte: <a href=\"https://t.me/nullvpn_net\" target=\"_blank\" rel=\"noopener\" referrerpolicy=\"no-referrer\">@nullvpn_net</a> o <a href=\"mailto:support@nullvpn.net\">support@nullvpn.net</a>.",
    ne: "GitHub बाट बाहिर निस्किएको छौं? <a href=\"https://t.me/nullvpn_net\" target=\"_blank\" rel=\"noopener\" referrerpolicy=\"no-referrer\">@nullvpn_net</a> मा समर्थनमा पुग्नुहोस् वा <a href=\"mailto:support@nullvpn.net\">support@nullvpn.net</a> मेल गर्नुहोस् — हामी छिटो प्रतिक्रिया दिन्छौं।",
    fr: "Bloqué sur GitHub ? Contactez l'assistance via <a href=\"https://t.me/nullvpn_net\" target=\"_blank\" rel=\"noopener\" referrerpolicy=\"no-referrer\">@nullvpn_net</a> ou <a href=\"mailto:support@nullvpn.net\">support@nullvpn.net</a>.",
  },
  "dl.hero.btn": {
    en: "Get it on GitHub Releases →",
    ru: "Забрать с GitHub Releases →",
    fa: "دریافت از GitHub Releases →",
    ar: "احصل عليه من GitHub Releases →",
    es: "Consíguela en GitHub Releases →",
    ne: "GitHub Releases मा लिनुहोस् →",
    fr: "L'obtenir sur GitHub Releases →",
  },
  "price.p1.amount": {
    en: "$3",
    ru: "300 ₽",
    fa: "$3",
    ar: "$3",
    es: "$3",
    ne: "$3",
    fr: "$3",
  },
  "price.p3.amount": {
    en: "$10",
    ru: "1 000 ₽",
    fa: "$10",
    ar: "$10",
    es: "$10",
    ne: "$10",
    fr: "$10",
  },
  "price.p4.amount": {
    en: "$35",
    ru: "3 500 ₽",
    fa: "$35",
    ar: "$35",
    es: "$35",
    ne: "$35",
    fr: "$35",
  },
  "footer.support": {
    en: "Support",
    ru: "Поддержка",
    fa: "پشتیبانی",
    ar: "الدعم",
    es: "Soporte",
    ne: "सहयोग",
    fr: "Assistance",
  },
  "contact.sup.h": {
    en: "Support",
    ru: "Поддержка",
    fa: "پشتیبانی",
    ar: "الدعم",
    es: "Soporte",
    ne: "सहयोग",
    fr: "Assistance",
  },
  "contact.sup.p": {
    en: "Questions about payment, connection, or your plan? Message us on Telegram or email — we respond fast.",
    ru: "Вопросы по оплате, подключению или тарифу? Напишите нам в Telegram или на почту — отвечаем быстро.",
    fa: "پرسشی درباره پرداخت، اتصال یا طرح دارید؟ در تلگرام یا ایمیل پیام دهید — سریع پاسخ می‌دهیم.",
    ar: "أسئلة عن الدفع أو الاتصال أو خطتك؟ راسلنا على Telegram أو البريد الإلكتروني — نرد بسرعة.",
    es: "¿Preguntas sobre el pago, la conexión o tu plan? Escríbenos por Telegram o correo — respondemos rápido.",
    ne: "भुक्तानी, जडान, वा तपाईंको योजनाबारे प्रश्नहरू? टेलिग्राममा हामीलाई मेसेज पठाउनुहोस् वा इमेल गर्नुहोस् — हामी छिटो प्रतिक्रिया दिन्छौं।",
    fr: "Des questions sur le paiement, la connexion ou votre forfait ? Écrivez-nous sur Telegram ou par e-mail — nous répondons vite.",
  },
  "contact.sup.tg.btn": {
    en: "Telegram: @nullvpn_net →",
    ru: "Телеграм: @nullvpn_net →",
    fa: "تلگرام: @nullvpn_net →",
    ar: "تيليجرام: @nullvpn_net →",
    es: "Telegram: @nullvpn_net →",
    ne: "टेलिग्राम: @nullvpn_net →",
    fr: "Telegram : @nullvpn_net →",
  },
  "contact.sup.em.btn": {
    en: "Email: support@nullvpn.net →",
    ru: "Почта: support@nullvpn.net →",
    fa: "ایمیل: support@nullvpn.net →",
    ar: "البريد: support@nullvpn.net →",
    es: "Correo: support@nullvpn.net →",
    ne: "इमेल: support@nullvpn.net →",
    fr: "E-mail : support@nullvpn.net →",
  },

};

  // ─────────────────────────────────────────────────────────────────────────────
  // ENGINE
  // ─────────────────────────────────────────────────────────────────────────────
  function getLang() {
    // r87: ?lang= deep link — a shared localized URL (e.g. /pricing.html?lang=ru)
    // must land in that language even on a fresh profile where neither
    // localStorage nor navigator.language agrees. Validated against the real
    // translation table via hasOwnProperty (a bare T['nav.home'][qp] read would
    // accept inherited keys like 'constructor'), persisted so the choice
    // survives navigation, then stripped from the address bar: the param is a
    // one-shot entry instruction, not state — keeping it would fight a later
    // explicit switch (a bookmark would carry a stale locale override).
    // Sibling params (?plan=, ?payment_id=, ?cat=, ?perf=) are preserved.
    try {
      const qp = new URLSearchParams(location.search).get('lang');
      if (qp && Object.prototype.hasOwnProperty.call(T['nav.home'], qp)) {
        try { localStorage.setItem(STORAGE_KEY, qp); } catch (_) { /* ignore */ }
        if (history.replaceState) {
          const u = new URL(location.href);
          u.searchParams.delete('lang');
          history.replaceState(null, '', u.pathname + u.search + u.hash);
        }
        return qp;
      }
    } catch (_) { /* no URLSearchParams/URL (old WebViews): fall through */ }
    try {
      const saved = localStorage.getItem(STORAGE_KEY);
      if (saved && T['nav.home'][saved]) return saved;
    } catch (_) { /* localStorage unavailable (e.g. TON Web3 / private mode) */ }
    // r135: scan the FULL preference list — navigator.language is only its
    // first entry. A 'de'-primary visitor whose list is ['de','ru'] has a
    // supported second choice ('ru'); serving it beats silently defaulting
    // to EN. First match wins (browser order = user preference order); the
    // 2-char base keeps matching consistent with the single-entry path.
    // No persistence here: the auto-detect stays a per-visit default so an
    // explicit language choice (stored above) always outranks it.
    const prefs = (navigator.languages && navigator.languages.length)
      ? navigator.languages
      : [navigator.language || ''];
    for (const pref of prefs) {
      const base = (pref || '').slice(0, 2).toLowerCase();
      if (T['nav.home'][base]) return base;
    }
    return DEFAULT_LANG;
  }

  function applyLang(lang) {
    const isRTL = RTL_LANGS.includes(lang);
    document.documentElement.lang = lang;
    document.documentElement.dir = isRTL ? 'rtl' : 'ltr';
    try { localStorage.setItem(STORAGE_KEY, lang); } catch (_) { /* ignore */ }

    document.querySelectorAll('[data-i18n]').forEach(el => {
      const key = el.getAttribute('data-i18n');
      if (T[key] && T[key][lang]) {
        if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
          el.placeholder = T[key][lang];
        } else {
          el.innerHTML = String(T[key][lang]).replace(/\{year\}/g, String(new Date().getFullYear()));
        }
      }
    });

    // update selector active state (data-lang is the robust match; aria-pressed for a11y)
    document.querySelectorAll('.lang-btn').forEach(btn => {
      const active = btn.getAttribute('data-lang') === lang;
      btn.classList.toggle('active', active);
      btn.setAttribute('aria-pressed', active ? 'true' : 'false');
    });

    // refresh engine-managed feature texts (back-to-top label, filter status, stamp)
    updateFeatureTexts(lang);

    // r121: reveal the navbar once the localized layout is committed. The
    // head locale-bootstrap hides .nav-inner (visibility — layout-neutral)
    // whenever a stored non-EN locale resolves, so the EN->locale text swap
    // and the RTL flip can never repaint already-painted chrome (measured
    // CLS 0.062-0.251 navbar shifts on warm SW-cached loads). Idempotent:
    // applyLang runs on every explicit language switch; the bootstrap also
    // carries a 2s failsafe reveal for the i18n-never-ran case.
    document.documentElement.classList.remove('nv-l');
  }

  // Expose setLang globally for inline onclick handlers
  window.setLang = function(lang) {
    applyLang(lang);
  };

  // ─────────────────────────────────────────────────────────────────────────────
  // FEATURE LAYER (r6): small site-wide UX features driven by the i18n engine
  // so every page gets them consistently. All are guarded by element existence.
  // ─────────────────────────────────────────────────────────────────────────────
  function t(key, lang) {
    const entry = T[key];
    if (!entry) return '';
    return entry[lang] || entry.en || '';
  }

  // 1) Back-to-top button — created once here so all 14 pages get it without
  //    markup changes. Hidden until 600px scroll; respects reduced motion.
  const backToTop = document.createElement('button');
  backToTop.className = 'back-to-top';
  backToTop.type = 'button';
  backToTop.setAttribute('aria-label', t('a11y.backtop', getLang()));
  backToTop.innerHTML = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 19V5"/><path d="m5 12 7-7 7 7"/></svg>';
  backToTop.addEventListener('click', () => {
    const reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' });
  });
  let bttTicking = false;
  window.addEventListener('scroll', () => {
    if (bttTicking) return;
    bttTicking = true;
    requestAnimationFrame(() => {
      backToTop.classList.toggle('show', window.scrollY > 600);
      bttTicking = false;
    });
  }, { passive: true });
  document.body.appendChild(backToTop);
  // 6) Scroll reveal (r39) — sections fade/slide in as they enter the
    //    viewport. No-JS users: body never gets .reveal-scope, so nothing
    //    is ever hidden. Reduced-motion users: CSS forces full visibility.
    if (window.matchMedia && !window.matchMedia('(prefers-reduced-motion: reduce)').matches
        && 'IntersectionObserver' in window) {
      document.body.classList.add('reveal-scope');
      const revealIo = new IntersectionObserver((entries) => {
        entries.forEach((en) => {
          if (en.isIntersecting) {
            en.target.classList.add('reveal-in');
            revealIo.unobserve(en.target);
          }
        });
      }, { threshold: 0.06, rootMargin: '0px 0px -5% 0px' });
      document.querySelectorAll('body > section, main > section').forEach((sec) => revealIo.observe(sec));
    }

  // Legal ToC scroll-spy (r53) — highlights the .page-toc pill of the section
  // currently in view (aria-current="location"). Cosmetic only: fully wrapped,
  // no-op on pages without a ToC. applyLang replaces link text only, so the
  // classes/attributes set here survive every language switch.
  try {
    const toc = document.querySelector('.page-toc');
    if (toc && 'IntersectionObserver' in window) {
      const tocLinks = Array.prototype.slice.call(toc.querySelectorAll('a[href^="#"]'));
      const spyMap = [];
      tocLinks.forEach((a) => {
        const sec = document.getElementById((a.getAttribute('href') || '').slice(1));
        if (sec) spyMap.push({ a: a, sec: sec });
      });
      if (spyMap.length) {
        const inBand = new Set();
        const spy = new IntersectionObserver((entries) => {
          entries.forEach((en) => {
            if (en.isIntersecting) inBand.add(en.target.id);
            else inBand.delete(en.target.id);
          });
          const hit = spyMap.filter((m) => inBand.has(m.sec.id))[0];
          if (!hit) return; // band between sections: keep last highlight (sticky)
          spyMap.forEach((m) => {
            const on = m === hit;
            m.a.classList.toggle('toc-active', on);
            if (on) m.a.setAttribute('aria-current', 'location');
            else m.a.removeAttribute('aria-current');
          });
        }, { rootMargin: '-45% 0px -50% 0px', threshold: 0 });
        spyMap.forEach((m) => spy.observe(m.sec));
      }
    }
  } catch (_) { /* cosmetic; never break the page */ }

  // 5) Copy-to-clipboard chips (contact page Support card) — copies the exact
  //    handle value, flips the chip icon to ✓ briefly, announces via aria-live.
  const copyChips = document.querySelectorAll('.copy-chip[data-copy]');
  if (copyChips.length) {
    let copyLive = document.getElementById('copyLive');
    if (!copyLive) {
      copyLive = document.createElement('div');
      copyLive.id = 'copyLive';
      copyLive.className = 'sr-only';
      copyLive.setAttribute('aria-live', 'polite');
      document.body.appendChild(copyLive);
    }
    copyChips.forEach((chip) => {
      chip.addEventListener('click', async () => {
        if (chip.dataset.copyBusy === '1') return;
        chip.dataset.copyBusy = '1';
        const val = chip.getAttribute('data-copy') || '';
        let ok = false;
        try { await navigator.clipboard.writeText(val); ok = true; }
        catch (_) {
          try {
            const ta = document.createElement('textarea');
            ta.value = val;
            ta.setAttribute('readonly', '');
            ta.style.position = 'fixed';
            ta.style.opacity = '0';
            document.body.appendChild(ta);
            ta.select();
            ok = document.execCommand('copy');
            document.body.removeChild(ta);
          } catch (_) { ok = false; }
        }
        chip.classList.add(ok ? 'copied' : 'copyfail');
        const ico = chip.querySelector('.copy-ico');
        if (ico) ico.textContent = ok ? '✓' : '⨯';
        copyLive.textContent = t(ok ? 'a11y.copied' : 'a11y.copyfail', getLang());
        setTimeout(() => {
          chip.classList.remove('copied', 'copyfail');
          if (ico) ico.textContent = '⧉';
          delete chip.dataset.copyBusy;
        }, 1600);
      });
    });
  }

  // 2) FAQ live filter — filters .faq-item blocks against the CURRENT locale's
  //    rendered text. Status is announced via aria-live for screen readers.
  const faqFilter = document.getElementById('faqFilter');
  let applyFaqFilter = null;
  let activeCat = 'all'; // r49: active FAQ category chip ('all' | .faq-item[data-cat] value)
  let lastFilterLang = null; // r100: boot guard for the language-switch query reset
  if (faqFilter) {
    // r96: capture a deep-linked ?q= BEFORE any filter run — applyFaqFilter
    // now owns the ?q= URL slot and would strip it on its first pass.
    const initialQ = (() => {
      try { return (new URLSearchParams(location.search).get('q') || '').slice(0, 80); }
      catch (_) { return ''; }
    })();
    const items = Array.from(document.querySelectorAll('.faq-item'));
    const status = document.getElementById('faqFilterStatus');
    const clearBtn = document.getElementById('faqFilterClear');
    const emptyEl = document.getElementById('faqEmpty'); // r56: no-results state
    const total = items.length;
    const norm = (s) => (s || '').toLowerCase().replace(/\s+/g, ' ').trim();
    // r57: search-hit highlighting — matches wrapped in <mark>. Text nodes are
    // collected first and wrapped after the walk (replacing nodes mid-walk
    // breaks a live TreeWalker). unmark() + parent.normalize() restores the
    // original nodes each run; applyLang wipes data-i18n text on language
    // switch and re-runs this filter, so highlights self-heal.
    const markRx = (q) => new RegExp(q.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi');
    const unmark = (root) => {
      root.querySelectorAll('mark').forEach((m) => {
        const p = m.parentNode;
        if (!p) return;
        p.replaceChild(document.createTextNode(m.textContent), m);
        p.normalize(); // re-merge adjacent text nodes the mark split
      });
    };
    const markHits = (root, rx) => {
      const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, null);
      const nodes = [];
      while (walker.nextNode()) if (walker.currentNode.nodeValue.trim()) nodes.push(walker.currentNode);
      nodes.forEach((n) => {
        const text = n.nodeValue;
        rx.lastIndex = 0;
        if (!rx.test(text)) return;
        rx.lastIndex = 0;
        const frag = document.createDocumentFragment();
        let last = 0, m;
        while ((m = rx.exec(text))) {
          if (m.index > last) frag.appendChild(document.createTextNode(text.slice(last, m.index)));
          const mk = document.createElement('mark');
          mk.textContent = m[0];
          frag.appendChild(mk);
          last = m.index + m[0].length;
        }
        if (last < text.length) frag.appendChild(document.createTextNode(text.slice(last)));
        n.parentNode.replaceChild(frag, n);
      });
    };
    applyFaqFilter = () => {
      const q = norm(faqFilter.value);
      let shown = 0;
      items.forEach((it) => {
        unmark(it); // r57: clear the previous run's highlights first
        const textHit = !q || norm(it.textContent).includes(q);
        const catHit = activeCat === 'all' || it.dataset.cat === activeCat;
        const hit = textHit && catHit;
        it.style.display = hit ? '' : 'none';
        if (hit) { shown++; if (q) markHits(it, markRx(q)); }
      });
      if (clearBtn) clearBtn.hidden = !faqFilter.value;
      // r56: empty state only when the user actually narrowed something down
      // (a query or an active category) and nothing survived the filter.
      if (emptyEl) emptyEl.hidden = !((q || activeCat !== 'all') && shown === 0);
      if (status) {
        const lang = document.documentElement.lang || 'en';
        status.classList.remove('is-note'); /* typing/filtering retires the r100 note */
        status.textContent = (q || activeCat !== 'all')
          ? t('faq.filter.results', lang).replace('{n}', shown).replace('{total}', total)
          : '';
      }
      // r96: keep ?q= in the URL — shareable filtered views (r50 did ?cat=).
      // replaceState: no history spam per keystroke. searchParams mutates in
      // place, so ?cat= (and any other params) are preserved.
      try {
        const u = new URL(location.href);
        if (q) u.searchParams.set('q', q);
        else u.searchParams.delete('q');
        history.replaceState(null, '', u);
      } catch (_) { /* sandboxed context: URL sync is cosmetic */ }
    };
    faqFilter.addEventListener('input', applyFaqFilter);
    // r95: Escape clears the filter through the canonical path (refilter + URL
    // sync + status + clear-chip hide). preventDefault also stops native
    // search-input clearing, which some engines fire without an input event —
    // that would desync the visible list from the (hidden) cancel button.
    faqFilter.addEventListener('keydown', (e) => {
      if (e.key !== 'Escape' || !faqFilter.value) return;
      e.preventDefault();
      faqFilter.value = '';
      applyFaqFilter();
      faqFilter.focus();
    });
    // r49: category chips — delegated listener on the row, bound once.
    // r50: the active category syncs to the URL (?cat=…) so filtered views are
    // shareable/deep-linkable; replaceState keeps history clean.
    const catRow = document.querySelector('.faq-cats');
    if (catRow) {
      const syncCatUrl = () => {
        try {
          const u = new URL(location.href);
          if (activeCat === 'all') u.searchParams.delete('cat');
          else u.searchParams.set('cat', activeCat);
          history.replaceState(null, '', u);
        } catch (_) { /* sandboxed context: URL sync is cosmetic */ }
      };
      const setActiveCat = (btn) => {
        activeCat = btn.dataset.cat || 'all';
        catRow.querySelectorAll('.faq-cat').forEach((b) => {
          const on = b === btn;
          b.classList.toggle('active', on);
          b.setAttribute('aria-pressed', on ? 'true' : 'false');
        });
        applyFaqFilter();
        syncCatUrl();
      };
      catRow.addEventListener('click', (e) => {
        const btn = e.target.closest('.faq-cat');
        if (!btn || !catRow.contains(btn)) return;
        setActiveCat(btn);
      });
      // r50: deep link — /faq.html?cat=pay pre-selects the Payments chip.
      try {
        const initial = new URLSearchParams(location.search).get('cat');
        if (initial && initial !== 'all') {
          const target = catRow.querySelector('.faq-cat[data-cat="' + initial + '"]');
          if (target) setActiveCat(target);
        }
      } catch (_) { /* malformed URL: default state stays */ }
    }
    if (clearBtn) {
      clearBtn.addEventListener('click', () => {
        faqFilter.value = '';
        applyFaqFilter();
        faqFilter.focus();
      });
    }
    // r56: empty-state "Reset filters" — clears the query and re-activates the
    // All chip through the existing delegated handler (re-filters + URL sync).
    const emptyReset = document.getElementById('faqEmptyReset');
    if (emptyReset) {
      emptyReset.addEventListener('click', () => {
        faqFilter.value = '';
        const allBtn = catRow && catRow.querySelector('.faq-cat[data-cat="all"]');
        if (allBtn) allBtn.click();
        else applyFaqFilter();
        faqFilter.focus();
      });
    }
    // r96: deep link — /faq.html?q=refund pre-fills + applies the search after
    // the ?cat= restore above, so combined views (?cat=pay&q=refund) resolve.
    if (initialQ) {
      faqFilter.value = initialQ;
      applyFaqFilter();
    }
  }

  // 2b) "/" keyboard shortcut — jump to FAQ search. Only when the page has
  //     a filter and the user is not already typing in a field.
  if (faqFilter) {
    document.addEventListener('keydown', (e) => {
      if (e.key !== '/' || e.ctrlKey || e.metaKey || e.altKey) return;
      const a = document.activeElement;
      const typing = a && (a.tagName === 'INPUT' || a.tagName === 'TEXTAREA' || a.isContentEditable);
      if (typing) return;
      e.preventDefault();
      // r95: honor prefers-reduced-motion — the back-to-top button already
      // gates its scrollTo; this jump was still force-animating for users who
      // opted out of motion at the OS level.
      const reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      faqFilter.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'center' });
      faqFilter.focus();
    });
  }

  // 2c) "/" shortcut on the 404 recovery search (r108) — parity with 2b.
  //     The form itself stays zero-JS; this only adds the keyboard
  //     affordance when scripting is live. Guard shape mirrors 2b.
  //     r109: Escape completes the keyboard loop — while the field is
  //     focused it clears the query and dismisses focus (the FAQ r95
  //     "Escape cancels search" language, adapted to the zero-JS form;
  //     preventDefault normalizes engines whose native search-Escape
  //     clears without an input event). "/" and Escape share one listener.
  const nfInput = document.querySelector('.nf-search input');
  if (nfInput) {
    document.addEventListener('keydown', (e) => {
      if (e.ctrlKey || e.metaKey || e.altKey) return;
      if (e.key === '/') {
        const a = document.activeElement;
        const typing = a && (a.tagName === 'INPUT' || a.tagName === 'TEXTAREA' || a.isContentEditable);
        if (typing) return;
        e.preventDefault();
        nfInput.focus();
      } else if (e.key === 'Escape' && document.activeElement === nfInput) {
        e.preventDefault();
        nfInput.value = '';
        nfInput.blur();
      }
    });
  }

  // 3) Capability "last verified" stamp — the date lives in a source-controlled
  //    <time datetime> attribute (updated by tools/stamp_verified.js); here we
  //    only localize its DISPLAY via Intl for the active locale. No-JS users
  //    see the static fallback text.
  // 4) Shared per-language updates for dynamically managed texts.
  function updateFeatureTexts(lang) {
    backToTop.setAttribute('aria-label', t('a11y.backtop', lang));
    const clearBtn = document.getElementById('faqFilterClear');
    if (clearBtn) clearBtn.setAttribute('aria-label', t('faq.filter.clear', lang));
    document.querySelectorAll('[data-i18n-aria]').forEach((chip) => {
      const aria = t(chip.getAttribute('data-i18n-aria'), lang) || chip.getAttribute('aria-label');
      chip.setAttribute('aria-label', aria);
      // r77: injected chips also carry a hover tooltip (r76) — keep it
      // mirroring the accessible name so both retranslate together.
      if (chip.hasAttribute('title')) chip.setAttribute('title', aria);
    });

    // 7b) FAQ permalink anchors (r42) — must run AFTER the [data-i18n] pass:
    //     h3 nodes are data-i18n targets, so their textContent rewrite wipes
    //     any anchor appended earlier; rebuilding here makes every pass
    //     self-healing. The per-item anchor check keeps this idempotent.
    if (document.querySelector('.faq-item[id]')) {
      // r76: on privacy/terms/refund the same .faq-item blocks are policy
      // clauses, not Q&A answers — name the chip for what it is so the
      // accessible label (and the r76 hover tooltip) matches the context.
      const isLegalPage = /\/(privacy|terms|refund)\.html$/.test(location.pathname);
      const chipAriaKey = isLegalPage ? 'share.clause' : 'share.answer';
      const anchorAriaKey = isLegalPage ? 'faq.anchor.clause' : 'faq.anchor.label';
      document.querySelectorAll('.faq-item[id]').forEach((item) => {
        item.setAttribute('tabindex', '-1'); // r51: deep-link targets accept fragment focus (SR announcement)
        const h3 = item.querySelector('h3');
        if (!h3 || h3.querySelector('.faq-anchor')) return;
        const qText = h3.textContent; // r65: question as share text — captured BEFORE the '#' anchor joins the h3
        const a = document.createElement('a');
        a.className = 'faq-anchor';
        a.href = '#' + item.id;
        a.setAttribute('data-i18n-aria', anchorAriaKey);
        a.setAttribute('aria-label', t(anchorAriaKey, lang));
        a.title = t(anchorAriaKey, lang); // r76: hover tooltip — icon-only affordances need a name on hover too
        a.textContent = '#';
        a.addEventListener('click', (ev) => {
          // r62: copying a permalink used to be completely silent (no live-region
          // announcement, no execCommand fallback — a rejected clipboard just
          // dumped the visitor on the answer with no link). Announce success
          // through #copyLive, fall back to execCommand, jump only on total fail.
          // r63: prefer the page's rel=canonical so links copied from /index.html
          // landings, filtered views (?cat=/?q=) or mirrors all consolidate to
          // the one primary URL; falls back to origin+pathname when absent.
          const can = document.querySelector('link[rel="canonical"]');
          const url = ((can && can.href) || (location.origin + location.pathname)) + '#' + item.id;
          let live = document.getElementById('copyLive');
          if (!live) {
            live = document.createElement('div');
            live.id = 'copyLive';
            live.className = 'sr-only';
            live.setAttribute('aria-live', 'polite');
            document.body.appendChild(live);
          }
          const done = () => {
            history.pushState(null, '', '#' + item.id);
            a.classList.add('copied');
            setTimeout(() => a.classList.remove('copied'), 1400);
            live.textContent = t('a11y.copied', getLang());
          };
          const legacyCopy = () => {
            try {
              const ta = document.createElement('textarea');
              ta.value = url;
              ta.setAttribute('readonly', '');
              ta.style.position = 'fixed';
              ta.style.opacity = '0';
              document.body.appendChild(ta);
              ta.select();
              const ok = document.execCommand('copy');
              document.body.removeChild(ta);
              return ok;
            } catch (_) { return false; }
          };
          if (navigator.clipboard && navigator.clipboard.writeText) {
            ev.preventDefault();
            navigator.clipboard.writeText(url)
              .then(done)
              .catch(() => { if (legacyCopy()) done(); else location.hash = item.id; });
          } else if (legacyCopy()) {
            ev.preventDefault();
            done();
          } // else: native jump — navigation itself is the feedback
        });
        h3.appendChild(a);

        // r65: per-answer share chip — a quiet icon-only .share-chip appended
        // to the answer paragraph. Shares the answer's canonical permalink
        // (page canonical + fragment) with the question as the share text.
        // Binding is NOT done here: the share engine (section 12) is now a
        // single delegated document-level listener, so these buttons — wiped
        // and rebuilt by every applyLang pass exactly like the anchors — are
        // picked up automatically, fresh DOM or not.
        const ansP = item.querySelector('p');
        if (ansP && !ansP.querySelector('.faq-share')) {
          const canEl = document.querySelector('link[rel="canonical"]');
          const shBtn = document.createElement('button');
          shBtn.type = 'button';
          shBtn.className = 'share-chip faq-share';
          shBtn.setAttribute('data-i18n-aria', chipAriaKey);
          shBtn.setAttribute('aria-label', t(chipAriaKey, lang));
          shBtn.title = t(chipAriaKey, lang); // r76: hover tooltip (matches the lang buttons' convention)
          shBtn.setAttribute(
            'data-share-url',
            ((canEl && canEl.href) || (location.origin + location.pathname)) + '#' + item.id
          );
          shBtn.setAttribute('data-share-text', qText);
          shBtn.innerHTML =
            '<span class="share-ico" aria-hidden="true">' +
            '<svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' +
            '<circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/>' +
            '<line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/>' +
            '</svg></span>';
          ansP.appendChild(shBtn);
        }
      });
    }

    // 7c) how-it-works step anchors (r110) — the narrative h2s gain stable
    //     slugs + hover permalink chips, mirroring 7b's FAQ machinery so
    //     support can deep-link straight to "Install the app" or "Tap
    //     Connect". The selector is id-scoped and document-wide: only the how page's
    //     h2s carry ids today, and any future page that adds an h2 id gets
    //     the same affordance automatically — one contract, no per-page list. Same self-healing
    //     contract as 7b: h2 nodes are data-i18n targets, so the anchor is
    //     rebuilt after every applyLang pass; the idempotence check keeps
    //     repeated passes from stacking chips.
    if (document.querySelector('h2[id]')) {
      document.querySelectorAll('h2[id]').forEach((h2) => {
        h2.setAttribute('tabindex', '-1'); // r51: fragment focus announces the step
        if (h2.querySelector('.faq-anchor')) return;
        const a = document.createElement('a');
        a.className = 'faq-anchor';
        a.href = '#' + h2.id;
        a.setAttribute('data-i18n-aria', 'faq.anchor.step');
        a.setAttribute('aria-label', t('faq.anchor.step', lang));
        a.title = t('faq.anchor.step', lang); // r76: hover tooltip — icon-only affordances need a name on hover
        a.textContent = '#';
        a.addEventListener('click', (ev) => {
          // r62/r63 machinery, verbatim contract: canonical permalink, live
          // region announcement, execCommand fallback, native jump on total fail.
          const can = document.querySelector('link[rel="canonical"]');
          const url = ((can && can.href) || (location.origin + location.pathname)) + '#' + h2.id;
          let live = document.getElementById('copyLive');
          if (!live) {
            live = document.createElement('div');
            live.id = 'copyLive';
            live.className = 'sr-only';
            live.setAttribute('aria-live', 'polite');
            document.body.appendChild(live);
          }
          const done = () => {
            history.pushState(null, '', '#' + h2.id);
            a.classList.add('copied');
            setTimeout(() => a.classList.remove('copied'), 1400);
            live.textContent = t('a11y.copied', getLang());
          };
          const legacyCopy = () => {
            try {
              const ta = document.createElement('textarea');
              ta.value = url;
              ta.setAttribute('readonly', '');
              ta.style.position = 'fixed';
              ta.style.opacity = '0';
              document.body.appendChild(ta);
              ta.select();
              const ok = document.execCommand('copy');
              document.body.removeChild(ta);
              return ok;
            } catch (_) { return false; }
          };
          if (navigator.clipboard && navigator.clipboard.writeText) {
            ev.preventDefault();
            navigator.clipboard.writeText(url)
              .then(done)
              .catch(() => { if (legacyCopy()) done(); else location.hash = h2.id; });
          } else if (legacyCopy()) {
            ev.preventDefault();
            done();
          } // else: native jump — navigation itself is the feedback
        });
        h2.appendChild(a);
      });
    }

    const stamp = document.getElementById('capVerifiedDate');
    if (stamp && stamp.dateTime) {
      try {
        // Gregorian calendar is forced even for fa/ar so the displayed date
        // stays directly comparable with the source-controlled datetime
        // attribute (what tools/stamp_verified.js writes).
        const locMap = { en: 'en-GB', ru: 'ru-RU', fa: 'fa-IR-u-ca-gregory', ar: 'ar-u-ca-gregory', es: 'es-ES', ne: 'ne-NP-u-ca-gregory', fr: 'fr-FR' };
        const d = new Date(stamp.dateTime + 'T00:00:00');
        stamp.textContent = new Intl.DateTimeFormat(locMap[lang] || 'en-GB', { year: 'numeric', month: 'long', day: 'numeric' }).format(d);
      } catch (_) { /* keep static fallback text */ }
    }
    // Dynamic copyright year — keeps "© <year>" current in every locale
    // without editing 7 translation strings each January. (r38)
    document.querySelectorAll('[data-i18n="footer.copy"]').forEach((el) => {
      el.textContent = el.textContent.replace(/\b20\d{2}\b/, String(new Date().getFullYear()));
    });
    // Download page: localized labels for the inline release-metadata
    // fetcher (it falls back to EN defaults until this map exists). (r38)
    if (document.getElementById('release-meta')) {
      window.DL_META_I18N = {
        version: t('dl.meta.version', lang),
        released: t('dl.meta.released', lang),
        package: t('dl.meta.package', lang),
        size: t('dl.meta.size', lang),
        minandroid: t('dl.meta.minandroid', lang),
        status: t('dl.meta.status', lang),
        stable: t('dl.meta.stable', lang),
      };
      // r112: labels follow the language immediately — re-render the already
      // rendered release grid (hook exists only on download.html; a guarded
      // no-op elsewhere). Re-renders the live release if the fetch landed,
      // else the static placeholder — either way with fresh labels.
      try { if (typeof window.RERENDER_RELEASE_META === 'function') window.RERENDER_RELEASE_META(); } catch (_) {}
    }
    // r92: re-run so the status line follows the active language. r100: a TEXT
    //     query cannot survive a language switch — matching is locale-text-
    //     based, so an EN term re-applied to RU text is a guaranteed 0-hit
    //     dead end with a foreign word left in the box. Clear it and say so
    //     (status is aria-live=polite); CATEGORY choices survive (data-cat is
    //     a locale-independent key). The FIRST pass (boot) must not clear —
    //     the r96 deep link restores ?q= in the wiring before this runs —
    //     hence the lastFilterLang boot guard.
    if (applyFaqFilter && faqFilter) {
      const langChanged = lastFilterLang !== null && lastFilterLang !== lang;
      lastFilterLang = lang;
      if (langChanged) {
        const hadQuery = !!faqFilter.value;
        if (hadQuery) faqFilter.value = '';
        applyFaqFilter();
        if (hadQuery && activeCat === 'all') {
          const statusEl = document.getElementById('faqFilterStatus');
          if (statusEl) {
            statusEl.classList.add('is-note');
            statusEl.textContent = t('faq.filter.cleared', lang);
            setTimeout(() => {
              if (statusEl.classList.contains('is-note')) {
                statusEl.classList.remove('is-note');
                statusEl.textContent = '';
              }
            }, 4000);
          }
        }
      } else if (faqFilter.value || activeCat !== 'all') {
        applyFaqFilter();
      }
    }

    // 11) Compare-table column spotlight (r59) — hovering any value cell tints
    //     its whole column so cross-row comparisons stay oriented in a 6-col
    //     table. Desktop pointers only (media check at bind time — touch
    //     devices never get listeners, mirroring the r53 hover doctrine).
    //     cellIndex is DOM order, so RTL locales spotlight the same logical
    //     column. The first column holds row labels — hovering it just clears.
    if (window.matchMedia && window.matchMedia('(hover: hover) and (pointer: fine)').matches) {
      const compTable = document.querySelector('.comp-table-wrap table');
      // r67: guard flag — updateFeatureTexts re-runs on every applyLang pass,
      // and the table element itself survives rebuilds, so re-binding here
      // stacked duplicate listeners (harmless but sloppy). One bind per table.
      if (compTable && !compTable.__r59spot) {
        compTable.__r59spot = true;
        let spotCol = -1;
        const unspot = () => {
          if (spotCol < 0) return;
          compTable.querySelectorAll('.comp-col-spot').forEach((el) => el.classList.remove('comp-col-spot'));
          spotCol = -1;
        };
        compTable.addEventListener('mouseover', (e) => {
          const cell = e.target.closest('td, th');
          if (!cell || !compTable.contains(cell)) { unspot(); return; }
          const idx = cell.cellIndex;
          if (idx === spotCol) return;
          unspot();
          if (idx === 0) return; // labels column: nothing to compare against
          spotCol = idx;
          Array.from(compTable.rows).forEach((tr) => {
            const c = tr.cells[idx];
            if (c) c.classList.add('comp-col-spot');
          });
        });
        compTable.addEventListener('mouseleave', unspot);
      }
    }

    // 14) Comparison column deep-links + per-column share chips (r66) — the
    //     r65 delegated share engine made per-chip URLs free, so each plan
    //     header (NullVPN / NordVPN / ExpressVPN / ProtonVPN / Self-hosted)
    //     gets a quiet icon chip that shares canonical + '#col-X', and
    //     arriving at such a URL pins the whole column with a persistent
    //     spotlight cousin (.comp-col-pin, styles inline in comparison.html
    //     next to the r59 hover rules). Pin mechanics are DOM-order cellIndex
    //     (r59 lesson: identical logical column in RTL); scrollIntoView
    //     brings an off-screen column into view on phones (RTL-safe natively).
    //     Chips are re-injected after every data-i18n pass (th textContent
    //     rewrites wipe them) with an idempotency check; the pin is idempotent
    //     class work that also survives rebuilds. The hashchange listener is
    //     bound ONCE (window flag, __swRegistered pattern).
      // r86: pricing plan + features row permalink chips — the estate-wide
      // completion of the r42 FAQ / r68 comparison convention. The r78/r79
      // deep-link ids and :target rings already exist; until now the only
      // way to SHARE them was hand-crafting the URL (the r81 404 rescue even
      // advertises /pricing.html#plan-annual — a recipient landing there saw
      // the ring but a pricing visitor had no visible way to produce that
      // link). Same doctrine end-to-end: canonical + fragment, clipboard →
      // execCommand → native jump, pushState (browsers re-evaluate :target
      // on fragment changes — the r42 chips have ridden this since r62),
      // .copied feedback, #copyLive announcement. Chips are wiped by every
      // applyLang pass (their host h3s are data-i18n targets) and rebuilt
      // here; the .faq-anchor presence check keeps it idempotent, and the
      // class is REUSED for its styling (:hover, :focus-visible, .copied
      // all come free — the h3s get the FAQ's flex layout page-locally).
      const makePermalinkChip = (host, id, ariaKey) => {
        const a = document.createElement('a');
        a.className = 'faq-anchor';
        a.href = '#' + id;
        a.setAttribute('data-i18n-aria', ariaKey);
        a.setAttribute('aria-label', t(ariaKey, lang));
        a.title = t(ariaKey, lang); // r76 convention: icon-only affordances need a hover name
        a.textContent = '#';
        a.addEventListener('click', (ev) => {
          const can = document.querySelector('link[rel="canonical"]');
          const url = ((can && can.href) || (location.origin + location.pathname)) + '#' + id;
          let live = document.getElementById('copyLive');
          if (!live) {
            live = document.createElement('div');
            live.id = 'copyLive';
            live.className = 'sr-only';
            live.setAttribute('aria-live', 'polite');
            document.body.appendChild(live);
          }
          const done = () => {
            history.pushState(null, '', '#' + id);
            a.classList.add('copied');
            setTimeout(() => a.classList.remove('copied'), 1400);
            live.textContent = t('a11y.copied', getLang());
          };
          const legacyCopy = () => {
            try {
              const ta = document.createElement('textarea');
              ta.value = url;
              ta.setAttribute('readonly', '');
              ta.style.position = 'fixed';
              ta.style.opacity = '0';
              document.body.appendChild(ta);
              ta.select();
              const ok = document.execCommand('copy');
              document.body.removeChild(ta);
              return ok;
            } catch (_) { return false; }
          };
          if (navigator.clipboard && navigator.clipboard.writeText) {
            ev.preventDefault();
            navigator.clipboard.writeText(url)
              .then(done)
              .catch(() => { if (legacyCopy()) done(); else location.hash = id; });
          } else if (legacyCopy()) {
            ev.preventDefault();
            done();
          } // else: native jump — navigation itself is the feedback
        });
        host.appendChild(a);
      };
      document.querySelectorAll('.pricing-card[id] h3').forEach((h3) => {
        if (h3.querySelector('.faq-anchor')) return;
        makePermalinkChip(h3, h3.closest('.pricing-card').id, 'pricing.anchor.plan');
      });
      document.querySelectorAll('.feat-body h3').forEach((h3) => {
        if (h3.querySelector('.faq-anchor')) return;
        const tr = h3.closest('tr[id]');
        if (!tr) return;
        makePermalinkChip(h3, tr.id, 'feat.anchor.row');
      });

    if (document.querySelector('.comp-table-wrap table')) {
      const compT2 = document.querySelector('.comp-table-wrap table');
      compT2.querySelectorAll('thead th[id]').forEach((th) => {
        th.classList.add('comp-colhead');
        if (th.querySelector('.comp-share')) return;
        const canEl = document.querySelector('link[rel="canonical"]');
        const b = document.createElement('button');
        b.type = 'button';
        b.className = 'share-chip faq-share comp-share';
        b.setAttribute('data-i18n-aria', 'comp.share.col');
        b.setAttribute('aria-label', t('comp.share.col', lang));
        b.title = t('comp.share.col', lang); // r76: hover tooltip, same convention as the faq/legal chips
        b.setAttribute(
          'data-share-url',
          ((canEl && canEl.href) || (location.origin + location.pathname)) + '#' + th.id
        );
        b.innerHTML =
          '<span class="share-ico" aria-hidden="true">' +
          '<svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' +
          '<circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/>' +
          '<line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/>' +
          '</svg></span>';
        th.appendChild(b);
      });
      const applyCompPin = () => {
        compT2.querySelectorAll('.comp-col-pin, tbody tr.comp-row-pin').forEach((el) => {
          el.classList.remove('comp-col-pin');
          el.classList.remove('comp-row-pin');
        });
        // r68: rows deep-link too — #row-<slug> pins the whole body row, the
        // row sibling of the r66 column pin (same tint family, inline CSS).
        const m = /^#(col-(nullvpn|nordvpn|expressvpn|protonvpn|selfhosted)|row-(works-strict|works-mobile|nologs|anonpay|noaccount|noappstore|obfuscation|autofailover|dedicated|reachable|setuptime))$/.exec(location.hash || '');
        if (!m) return;
        if (m[0].indexOf('#col-') === 0) {
          const th = compT2.querySelector('thead th#' + m[1]); // th ids carry the col- prefix
          if (!th) return;
          const idx = th.cellIndex;
          Array.from(compT2.rows).forEach((tr) => {
            const c = tr.cells[idx];
            if (c) c.classList.add('comp-col-pin');
          });
          try { th.scrollIntoView({ inline: 'center', block: 'nearest' }); }
          catch (_) { th.scrollIntoView(); } // very old browsers: vertical-only jump
        } else {
          const tr = compT2.querySelector('tbody tr#' + m[1]); // tr ids carry the row- prefix
          if (!tr) return;
          tr.classList.add('comp-row-pin');
          try { tr.scrollIntoView({ block: 'center' }); }
          catch (_) { tr.scrollIntoView(); }
        }
      };
      applyCompPin();
      if (!window.__compPinBound) {
        window.__compPinBound = true;
        window.addEventListener('hashchange', applyCompPin);
      }

      // r68: row permalink anchors — a quiet '#' beside each row label, the
      // comparison sibling of the r42 FAQ anchors. Click = copy canonical +
      // '#row-<slug>' (clipboard → execCommand → native jump fallbacks, same
      // doctrine), pushState + pin the row so the sharer sees what the
      // recipient will see, announce through #copyLive. Rebuilt after every
      // data-i18n pass (td textContent rewrite wipes them), idempotent.
      compT2.querySelectorAll('tbody tr[id]').forEach((tr) => {
        const label = tr.cells[0];
        if (!label || label.querySelector('.row-anchor')) return;
        const a = document.createElement('a');
        a.className = 'row-anchor';
        a.href = '#' + tr.id;
        a.setAttribute('data-i18n-aria', 'comp.anchor.row');
        a.setAttribute('aria-label', t('comp.anchor.row', lang));
        a.title = t('comp.anchor.row', lang); // r76: hover tooltip, same convention as the faq/legal chips
        a.textContent = '#';
        a.addEventListener('click', (ev) => {
          const canEl = document.querySelector('link[rel="canonical"]');
          const url = ((canEl && canEl.href) || (location.origin + location.pathname)) + '#' + tr.id;
          let live = document.getElementById('copyLive');
          if (!live) {
            live = document.createElement('div');
            live.id = 'copyLive';
            live.className = 'sr-only';
            live.setAttribute('aria-live', 'polite');
            document.body.appendChild(live);
          }
          const done = () => {
            history.pushState(null, '', '#' + tr.id); // no hashchange → pin manually
            applyCompPin();
            a.classList.add('copied');
            setTimeout(() => a.classList.remove('copied'), 1400);
            live.textContent = t('a11y.copied', getLang());
          };
          const legacyCopy = () => {
            try {
              const ta = document.createElement('textarea');
              ta.value = url;
              ta.setAttribute('readonly', '');
              ta.style.position = 'fixed';
              ta.style.opacity = '0';
              document.body.appendChild(ta);
              ta.select();
              const ok = document.execCommand('copy');
              document.body.removeChild(ta);
              return ok;
            } catch (_) { return false; }
          };
          if (navigator.clipboard && navigator.clipboard.writeText) {
            ev.preventDefault();
            navigator.clipboard.writeText(url)
              .then(done)
              .catch(() => { if (legacyCopy()) done(); else location.hash = tr.id; });
          } else if (legacyCopy()) {
            ev.preventDefault();
            done();
          } // else: native jump — hashchange fires, applyCompPin pins via listener
        });
        label.appendChild(a);
      });

      // r73: text export — the comparison as a chat-pasteable plain-text
      // summary (Telegram audience). Built from the CURRENT localized DOM on
      // every click, so the text always matches the active language: localized
      // h1, canonical URL attribution, then one block per row (localized label
      // + per-plan verdicts headed by the localized plan names). The chip is
      // STATIC in comparison.html and deliberately NOT a .share-chip (the
      // delegated engine would share the page URL instead) — bind ONCE with a
      // window flag; applyLang only rewrites the label span inside it.
      const copyChip = document.querySelector('.copy-text-chip');
      if (copyChip && !window.__compCopyBound) {
        window.__compCopyBound = true;
        copyChip.addEventListener('click', () => {
          const buildText = () => {
            const h1 = document.querySelector('h1'); // one h1 per page, localized
            const canEl = document.querySelector('link[rel="canonical"]');
            const lines = [];
            // innerText (not textContent): the h1 holds a <br> between its two
            // spans; innerText renders it as a newline so the collapse below
            // produces "NullVPN vs. the rest." instead of "vs.the rest."
            if (h1) lines.push(h1.innerText.replace(/\s+/g, ' ').trim());
            lines.push((canEl && canEl.href) || (location.origin + location.pathname));
            lines.push('');
            const heads = Array.from(compT2.tHead.rows[0].cells).slice(1).map((c) => c.textContent.trim());
            Array.from(compT2.tBodies[0].rows).forEach((tr) => {
              // the label cell carries the injected .row-anchor '#' — clone + strip
              // it so the exported text is clean (r73 self-review fix)
              const labelCell = tr.cells[0].cloneNode(true);
              const anc = labelCell.querySelector('.row-anchor');
              if (anc) anc.remove();
              const label = labelCell.textContent.replace(/\s+/g, ' ').trim();
              const vals = Array.from(tr.cells).slice(1)
                .map((c, i) => (heads[i] ? heads[i] + ' ' : '') + c.textContent.replace(/\s+/g, ' ').trim())
                .join(' | ');
              lines.push(label + '\n' + vals);
            });
            return lines.join('\n');
          };
          const text = buildText();
          let live = document.getElementById('copyLive');
          if (!live) {
            live = document.createElement('div');
            live.id = 'copyLive';
            live.className = 'sr-only';
            live.setAttribute('aria-live', 'polite');
            document.body.appendChild(live);
          }
          const done = (ok) => {
            copyChip.classList.add(ok ? 'copied' : 'copyfail');
            live.textContent = t(ok ? 'a11y.copied' : 'a11y.copyfail', getLang());
            if (ok && navigator.vibrate) {
              try { navigator.vibrate(8); } catch (_) { /* never block feedback */ }
            }
            setTimeout(() => copyChip.classList.remove('copied', 'copyfail'), 1600);
          };
          const legacyCopy = () => {
            try {
              const ta = document.createElement('textarea');
              ta.value = text;
              ta.setAttribute('readonly', '');
              ta.style.position = 'fixed';
              ta.style.opacity = '0';
              document.body.appendChild(ta);
              ta.select();
              const ok = document.execCommand('copy');
              document.body.removeChild(ta);
              return ok;
            } catch (_) { return false; }
          };
          if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(text)
              .then(() => done(true))
              .catch(() => done(legacyCopy()));
          } else {
            done(legacyCopy());
          }
        });
      }
    }

    // 15) Offline page inventory + auto-reconnect (r69) — offline.html only.
    //     The SW runtime-caches every HTML navigation that succeeds (r58),
    //     and offline.html's sub-copy already promises "pages you already
    //     visited may still be available"; this makes that promise real:
    //     enumerate the SW cache, keep same-origin document navigations from
    //     the known-pages allowlist, dedupe by pathname ('/' beats
    //     /index.html; ?cat= variants collapse), and render localized chips
    //     (labels reuse the nav./footer. keys — zero new per-page vocabulary).
    //     Enumeration runs ONCE (window.__ofPages promise); applyLang
    //     re-renders from the resolved list so chips follow setLang like all
    //     other engine-managed text. Hidden entirely when nothing is listable
    //     (fresh visitor, no SW yet). The 'online' listener shows a localized
    //     "back online" pill and reloads ~900ms later — no manual retry tap.
    const ofWrap = document.getElementById('ofWrap');
    if (ofWrap && typeof caches !== 'undefined') {
      const OF_PAGES = {
        '/': 'nav.home',
        '/index.html': 'nav.home',
        '/faq.html': 'nav.faq',
        '/pricing.html': 'nav.pricing',
        '/features.html': 'nav.features',
        '/how-it-works.html': 'nav.how',
        '/download.html': 'nav.download',
        '/contact.html': 'nav.contact',
        '/comparison.html': 'nav.compare',
        '/web3.html': null, // brand page: static label, no key
        '/terms.html': 'footer.terms',
        '/privacy.html': 'footer.privacy',
        '/refund.html': 'footer.refund',
      };
      if (!window.__ofPages) {
        window.__ofPages = caches.keys().then((keys) =>
          Promise.all(keys.map((k) => caches.open(k).then((c) => c.keys())))
            .then((lists) => {
              const paths = new Set();
              lists.flat().forEach((req) => {
                try {
                  const u = new URL(req.url);
                  if (u.origin !== location.origin) return;
                  if (u.pathname === '/offline.html') return;
                  if (!(u.pathname in OF_PAGES)) return;
                  if (req.mode && req.mode !== 'navigate' && (req.headers.get('accept') || '').indexOf('text/html') === -1) return;
                  paths.add(u.pathname);
                } catch (_) { /* skip malformed key */ }
              });
              const list = Array.from(paths);
              // '/' and '/index.html' are the same page — keep '/'
              if (list.indexOf('/index.html') !== -1 && list.indexOf('/') !== -1) {
                list.splice(list.indexOf('/index.html'), 1);
              }
              list.sort((a, b) => (a === '/' ? -1 : b === '/' ? 1 : a.localeCompare(b)));
              return list;
            })
            .catch(() => [])
        );
      }
      const renderOfList = (list) => {
        const ul = document.getElementById('ofList');
        if (!ul) return;
        if (!list.length) { ofWrap.hidden = true; return; }
        ofWrap.hidden = false;
        ul.innerHTML = '';
        list.forEach((p) => {
          const li = document.createElement('li');
          const a = document.createElement('a');
          a.href = p;
          const key = OF_PAGES[p];
          if (key) {
            const span = document.createElement('span');
            span.setAttribute('data-i18n', key);
            span.textContent = t(key, getLang());
            a.appendChild(span);
          } else {
            a.textContent = 'Web3'; // brand name — locale-independent
          }
          li.appendChild(a);
          ul.appendChild(li);
        });
      };
      window.__ofPages.then((list) => {
        window.__ofPagesResolved = list;
        renderOfList(list);
      });
      // re-render on language switches once the list has resolved
      if (window.__ofPagesResolved) renderOfList(window.__ofPagesResolved);
      const ofLive = document.getElementById('ofLive');
      if (ofLive && !window.__ofOnlineBound) {
        window.__ofOnlineBound = true;
        window.addEventListener('online', () => {
          // r97: verify the connection is real before promising anything —
          // the 'online' event fires on radio wake-up even when the network
          // is still unusable. HEAD is not GET, so the SW passes the probe
          // straight through to the network; no-store avoids HTTP caches.
          fetch('/', { method: 'HEAD', cache: 'no-store' })
            .then((r) => {
              if (!r.ok) return;
              ofLive.textContent = t('offline.backonline', getLang());
              ofLive.hidden = false;
              setTimeout(() => location.reload(), 900); // let the pill paint first
            })
            .catch(() => { /* still offline: stay silent, listener re-arms */ });
        });
      }
    }

    // 16) ?perf=1 Web Vitals HUD (r70) — maintainer diagnostics, zero cost and
    //     zero DOM when the query param is absent. Collects FCP, LCP (final
    //     entry wins), CLS (excluding recent-input shifts), request count and
    //     transfer size, plus service-worker control state, then paints a
    //     non-interactive glass chip (aria-hidden, pointer-events:none so it
    //     can never block the page) and mirrors a one-line summary to the
    //     console. Numeric labels are locale-independent developer output, not
    //     visitor content — intentionally untranslated. Observers are created
    //     with buffered:true so entries preceding the deferred script still
    //     count; the chip refreshes once 2.5s after load when LCP/CLS have
    //     mostly settled. r123: context segment (page/lang/dir @ host) —
    //     two rounds of HUD probes (r122 web3, r123 carried-locale) lost
    //     triage time to readings whose origin/locale had to be inferred;
    //     the chip now self-identifies (also exposes cross-origin redirects
    //     instantly: host flips to tonviewer.com on the web3 bridge).
    if (location.search.indexOf('perf=1') !== -1 && window.PerformanceObserver) {
      try {
        const pv = { fcp: 0, lcp: 0, cls: 0, reqs: 0, bytes: 0 };
        new PerformanceObserver((list) => {
          list.getEntries().forEach((e) => {
            if (e.name === 'first-contentful-paint') pv.fcp = Math.round(e.startTime);
          });
        }).observe({ type: 'paint', buffered: true });
        new PerformanceObserver((list) => {
          const es = list.getEntries();
          if (es.length) pv.lcp = Math.round(es[es.length - 1].startTime);
        }).observe({ type: 'largest-contentful-paint', buffered: true });
        new PerformanceObserver((list) => {
          list.getEntries().forEach((e) => {
            if (!e.hadRecentInput) pv.cls += e.value;
          });
        }).observe({ type: 'layout-shift', buffered: true });
        const renderHud = () => {
          const res = performance.getEntriesByType('resource');
          pv.reqs = res.length;
          pv.bytes = Math.round(res.reduce((s, r) => s + (r.transferSize || 0), 0) / 1024);
          const nav = performance.getEntriesByType('navigation')[0];
          const dcl = nav ? Math.round(nav.domContentLoadedEventEnd) : 0;
          const sw = navigator.serviceWorker && navigator.serviceWorker.controller ? 'controlled' : 'no sw';
          const hud = document.createElement('div');
          hud.className = 'perf-hud';
          hud.setAttribute('aria-hidden', 'true');
          hud.textContent =
            'LCP ' + pv.lcp + 'ms · FCP ' + pv.fcp + 'ms · DCL ' + dcl + 'ms' +
            ' | CLS ' + pv.cls.toFixed(3) +
            ' | ' + pv.reqs + ' req / ' + pv.bytes + 'KB' +
            ' | ' + sw +
            ' | ' + (document.documentElement.lang || '?') + '/' + (document.documentElement.dir || '?') +
            ' @ ' + location.host + '/' + (location.pathname.split('/').pop() || '');
          document.body.appendChild(hud);
          try { console.info('[perf]', hud.textContent); } catch (_) { /* old consoles */ }
        };
        if (document.readyState === 'complete') setTimeout(renderHud, 2500);
        else window.addEventListener('load', () => setTimeout(renderHud, 2500));
      } catch (_) { /* never break the page for diagnostics */ }
    }

    // 7) Service worker (r41) — offline support + faster repeat visits.
    //    Registered once per page load, secure origins only; /sw.js is
    //    network-first for HTML (fresh deploys always win) and cache-first
    //    for buster-versioned assets (a new ?v= is a new cache entry).
    if ('serviceWorker' in navigator && location.protocol === 'https:' && !window.__swRegistered) {
      window.__swRegistered = true;
      navigator.serviceWorker.register('/sw.js').catch(function () {});
    }
  }

  // Apply translations IMMEDIATELY when script loads (not waiting for DOMContentLoaded)
  // This prevents flash of untranslated content or raw translation keys
  // (applyLang also runs updateFeatureTexts at the end)
  // 8) Theme crossfade arming (r43): html.theme-anim enables the
  //    background/color transition declared in style.css. Armed two frames
  //    after load so the persisted theme applies instantly on navigation
  //    (no light-to-dark fade-in) while later manual toggles animate.
  try {
    if (!document.documentElement.classList.contains('theme-anim')) {
      requestAnimationFrame(function () {
        requestAnimationFrame(function () {
          document.documentElement.classList.add('theme-anim');
        });
      });
    }
  } catch (_) { /* very old browsers: theme switches stay instant */ }

  // 9) PWA install affordance (r45) — download page only. Chrome/Edge fire
  //    beforeinstallprompt once the SW + manifest criteria are met; we reveal
  //    a localized ghost CTA that defers the native install prompt to a user
  //    click. Mounted once at load (NOT inside updateFeatureTexts) so language
  //    switches never stack duplicate listeners; the button's textContent is
  //    rewritten by the data-i18n pass while the element itself persists.
  //    r132: zero-CLS repeat views. BIP capability is remembered in
  //    localStorage ('nv_bip'); download.html's head boot adds html.bip-ready
  //    pre-parse when the flag is set and the view is not standalone, and
  //    style.css overrides the UA [hidden] rule so the CTA occupies its layout
  //    slot at FIRST PAINT — the r131 root cause (post-paint reveal re-wraps
  //    .dh-cta, 0.010 CLS every repeat visit) becomes structurally impossible
  //    there. First-ever views keep the r45 reveal (BIP arrives post-paint;
  //    that single shift is the accepted cost of progressive enhancement).
  //    Flag lifecycle (all paths inside try/catch — private mode tolerated):
  //    BIP sets it; appinstalled, dead-click (pre-revealed but no prompt),
  //    the 4s no-BIP timeout, and standalone launches clear it, so the flag
  //    can never keep a dead button alive across sessions.
  try {
    var nvInstallEvt = null;
    var nvBipArrived = false; // r132: true only when BIP fired THIS load
    var nvInstallBtn = document.getElementById('dl-install');
    if (nvInstallBtn) {
      var nvBipFlag = function (on) {
        try {
          if (on) localStorage.setItem('nv_bip', '1');
          else localStorage.removeItem('nv_bip');
        } catch (_) {}
      };
      var nvBipHide = function () {
        document.documentElement.classList.remove('bip-ready');
        nvInstallBtn.hidden = true;
      };
      window.addEventListener('beforeinstallprompt', function (e) {
        e.preventDefault();
        nvInstallEvt = e;
        nvBipArrived = true;
        nvBipFlag(true);
        nvInstallBtn.hidden = false;
      });
      nvInstallBtn.addEventListener('click', function () {
        var evt = nvInstallEvt;
        nvInstallEvt = null;
        nvBipHide();
        if (evt && typeof evt.prompt === 'function') {
          try { evt.prompt(); } catch (_) {}
          try {
            if (evt.userChoice && typeof evt.userChoice.then === 'function') {
              evt.userChoice.catch(function () {});
            }
          } catch (_) {}
        } else {
          nvBipFlag(false); // r132: pre-revealed but BIP never came — self-heal
        }
      });
      window.addEventListener('appinstalled', function () {
        nvBipFlag(false);
        nvBipHide();
      });
      var nvBipArmed = false;
      try { nvBipArmed = localStorage.getItem('nv_bip') === '1'; } catch (_) {}
      var nvStandalone = false;
      try {
        nvStandalone = !!(window.matchMedia &&
          window.matchMedia('(display-mode: standalone)').matches);
      } catch (_) {}
      if (nvStandalone) {
        // Launched from the installed app: BIP cannot fire here; the flag is
        // stale by definition. Synchronous clear (head boot already skipped
        // adding bip-ready), button never flashes.
        nvBipFlag(false);
        nvBipHide();
      } else if (nvBipArmed) {
        setTimeout(function () {
          // r132: judge by nvBipArrived ONLY — under the CSS pre-reveal the
          // [hidden] property can be true while the CTA is visually revealed
          // (the .bip-ready rule outranks the attribute), so the property is
          // NOT a "user already dealt with it" signal. nvBipHide is idempotent:
          // if the user already clicked, the class is gone and this no-ops.
          if (!nvBipArrived) {
            nvBipHide();
            nvBipFlag(false);
          }
        }, 4000);
      }
    }
  } catch (_) { /* very old browsers: no install affordance */ }

  // 10) Scroll progress bar (r46) — decorative accent bar whose width tracks
  //     reading progress. rAF-throttled passive scroll listener; no-op on
  //     pages shorter than the viewport; aria-hidden, hidden in print, and
  //     mirrored to the right edge in RTL by style.css.
  try {
    var spBar = document.createElement('div');
    spBar.id = 'scroll-progress';
    spBar.setAttribute('aria-hidden', 'true');
    document.body.appendChild(spBar);
    var spTick = false;
    var spUpdate = function () {
      spTick = false;
      var max = document.documentElement.scrollHeight - window.innerHeight;
      var y = window.scrollY || document.documentElement.scrollTop || 0;
      var p = max > 0 ? Math.min(1, Math.max(0, y / max)) : 0;
      spBar.style.width = (p * 100).toFixed(2) + '%';
    };
    window.addEventListener('scroll', function () {
      if (!spTick) { spTick = true; requestAnimationFrame(spUpdate); }
    }, { passive: true });
    window.addEventListener('resize', spUpdate);
    spUpdate();
  } catch (_) { /* no progress bar on very old browsers */ }

  // 10b) Exact anchor offset (r80) — measure the real navbar height into the
  //      --nav-h CSS custom property. The navbar is NOT a constant across the
  //      estate: it stacks to 4 rows on the legal pages (~165px desktop) and
  //      wraps to 224-269px on mobile (locale-dependent), so fixed
  //      scroll-margin values (r41: 84px/168px) landed deep-link targets up
  //      to ~100px UNDER it. style.css consumes calc(var(--nav-h) + 50px);
  //      this block keeps --nav-h exact across viewport changes, font swaps
  //      and locale switches (RU/FR labels rewrap the bar). ResizeObserver
  //      covers every cause with one subscription; the resize-listener
  //      fallback covers ancient browsers. Guarded — no navbar, no-op.
  try {
    var nvBar = document.querySelector('.navbar');
    if (nvBar) {
      var nvSetH = function () {
        document.documentElement.style.setProperty('--nav-h', nvBar.offsetHeight + 'px');
      };
      nvSetH();
      if (typeof ResizeObserver !== 'undefined') {
        new ResizeObserver(nvSetH).observe(nvBar);
      } else {
        window.addEventListener('resize', nvSetH, { passive: true });
      }
    }
  } catch (_) { /* static fallback margins on very old browsers */ }

  // 12) Web share chips (r61; r65 delegated rewrite) — one tap opens the
  //     native share sheet when the browser offers one (navigator.share, most
  //     mobile browsers + desktop Chrome/Edge); otherwise the chip's URL is
  //     copied to the clipboard and the chip reuses the copy-chip feedback
  //     language (accent border + ✓, aria-live announcement). User-cancelled
  //     share sheets stay silent — cancelling is not a failure. The chip is a
  //     leaf-label button (label span carries data-i18n; icon is a sibling) so
  //     applyLang never wipes the icon.
  //     r65 rewrite: ONE delegated document-level listener replaces per-chip
  //     binding at eval time. Chips injected later by JS — e.g. the FAQ
  //     per-answer chips that applyLang wipes and rebuilds on every language
  //     switch — are picked up automatically without re-binding. Per-chip
  //     overrides via data attributes: data-share-url (default: the page's
  //     clean rel=canonical URL — r63 — so shared links survive UTM-free
  //     round trips; per-answer chips pass canonical + '#faq-N') and
  //     data-share-text (default: share.text; per-answer chips pass the
  //     localized question).
  try {
    var shLive = document.getElementById('copyLive');
    if (!shLive) {
      shLive = document.createElement('div');
      shLive.id = 'copyLive';
      shLive.setAttribute('aria-live', 'polite');
      shLive.setAttribute('role', 'status');
      shLive.style.position = 'absolute';
      shLive.style.width = '1px';
      shLive.style.height = '1px';
      shLive.style.overflow = 'hidden';
      shLive.style.clip = 'rect(0 0 0 0)';
      document.body.appendChild(shLive);
    }
    document.addEventListener('click', function (ev) {
      var chip = (ev.target && ev.target.closest) ? ev.target.closest('.share-chip') : null;
      if (!chip) return;
      {
          if (chip.dataset.shareBusy) return;
          chip.dataset.shareBusy = '1';
          var lang = getLang();
          // r63: prefer rel=canonical (see FAQ anchor note) — shared URLs must
          // be the primary one even from /index.html or ?cat=/ parameterized views.
          // r65: data-share-url overrides (per-answer chips: canonical + fragment).
          var can = document.querySelector('link[rel="canonical"]');
          var url = chip.getAttribute('data-share-url') ||
                    (can && can.href) || (location.origin + location.pathname);
          var shareTxt = chip.getAttribute('data-share-text') || t('share.text', lang);
          var shDone = function (ok) {
            chip.classList.add(ok ? 'copied' : 'copyfail');
            shLive.textContent = t(
              ok ? (chip.dataset.shareDone ? 'share.done' : 'a11y.copied') : 'a11y.copyfail',
              lang
            );
            // r72: a subtle 8ms tick on success — mobile-only affordance
            // (navigator.vibrate is a no-op on desktops), fires inside the
            // click gesture so it satisfies the user-activation rule.
            if (ok && navigator.vibrate) {
              try { navigator.vibrate(8); } catch (_) { /* never block feedback */ }
            }
            setTimeout(function () {
              chip.classList.remove('copied', 'copyfail');
              delete chip.dataset.shareBusy;
            }, 1600);
          };
          var shCopy = function () {
            try {
              if (navigator.clipboard && navigator.clipboard.writeText) {
                navigator.clipboard.writeText(url).then(
                  function () { shDone(true); },
                  function () { shDone(false); }
                );
                return;
              }
            } catch (_) { /* fall through to execCommand */ }
            var ok = false;
            try {
              var ta = document.createElement('textarea');
              ta.value = url;
              ta.style.opacity = '0';
              document.body.appendChild(ta);
              ta.select();
              ok = document.execCommand('copy');
              document.body.removeChild(ta);
            } catch (_) { ok = false; }
            shDone(ok);
          };
          try {
            if (navigator.share) {
              chip.dataset.shareDone = '1';
              navigator.share({
                title: document.title,
                text: shareTxt,
                url: url,
              }).then(function () {
                shDone(true);
              }).catch(function (e) {
                delete chip.dataset.shareDone;
                if (e && e.name === 'AbortError') {
                  delete chip.dataset.shareBusy; // cancelled: no feedback
                  return;
                }
                shCopy();
              });
              return;
            }
          } catch (_) { /* very old browsers: straight to clipboard */ }
          shCopy();
      }
    });
  } catch (_) { /* share chips never break the page */ }

  // 13) Browser-chrome theme sync (r64) — the static meta theme-color pair
  //     follows the OS (prefers-color-scheme), not the site toggle: a
  //     light-OS visitor who picks site-dark kept a champagne address bar
  //     fighting the page. Once the theme bootstrap has resolved data-theme,
  //     collapse to a single dynamic meta and mirror every change (initial
  //     + any later toggle) via attribute observation. No-JS visitors keep
  //     the static pair.
  try {
    const tcMeta = document.querySelector('meta[name="theme-color"]:not([media])');
    if (tcMeta) {
      const CHROME = { light: '#f7e7ce', dark: '#0a0f1a' };
      const syncChrome = () => {
        const t = document.documentElement.getAttribute('data-theme');
        if (t !== 'light' && t !== 'dark') return;
        tcMeta.setAttribute('content', CHROME[t]);
        document.querySelectorAll('meta[name="theme-color"][media]').forEach((m) => m.remove());
      };
      syncChrome();
      new MutationObserver(syncChrome).observe(document.documentElement, {
        attributes: true,
        attributeFilter: ['data-theme'],
      });
    }
  } catch (_) { /* chrome sync never breaks the page */ }

  // 14) Live OS-theme follow (r99) — visitors who never picked a theme get
  //     native-app behavior: the page re-themes the moment the OS flips
  //     (sunset schedule, manual dark-mode toggle in system settings). An
  //     explicit choice (stored 'theme') always wins and is never overrid-
  //     den. The r43 crossfade animates the change (it is reduced-motion
  //     gated) and the r64 chrome observer mirrors it into the address bar.
  try {
    const mqOS = window.matchMedia ? window.matchMedia('(prefers-color-scheme: dark)') : null;
    if (mqOS) {
      const osFollow = (e) => {
        try {
          if (localStorage.getItem('theme')) return; /* explicit choice wins */
          const t = e.matches ? 'dark' : 'light';
          document.documentElement.setAttribute('data-theme', t);
          if (typeof updateThemeButtons === 'function') updateThemeButtons(t);
        } catch (_) { /* storage denied: attribute-only follow */ }
      };
      if (mqOS.addEventListener) mqOS.addEventListener('change', osFollow);
      else if (mqOS.addListener) mqOS.addListener(osFollow); /* old Safari */
    }
  } catch (_) { /* OS follow never breaks the page */ }

  // 15) QR "open on your phone" card (r134) — download page only. The APK
  //     installs on Android, but the visitor is often reading on a desktop:
  //     a locally-generated QR of the page's rel=canonical (r63 pattern —
  //     never a per-locale/query variant) bridges the gap with zero network
  //     calls (privacy stance: no third-party QR image services). The encoder
  //     is self-contained (byte mode, ECC M, versions 2-3, full 8-mask
  //     penalty selection) and was verified decode-exact against the python
  //     qrcode reference AND two independent decoders (cv2, zbar) before
  //     shipping. Built SYNCHRONOUSLY at engine eval (defer = pre-paint), so
  //     the card cannot shift layout (CLS by construction, the r131/r132
  //     lesson). Desktop-only display (pointer:fine + width) — a phone does
  //     not scan itself. Any failure leaves the card absent: try/catch.
  try {
    if (/\/download\.html$/.test(location.pathname) && document.querySelector('.dl-hero .container')) {
      var qrCan = null;
      var nvQrUrl = (document.querySelector('link[rel="canonical"]') || {}).href ||
                    (location.origin + '/download.html');
      nvQrUrl = nvQrUrl.split('#')[0];
      var nvQr = (function () {
        /* --- self-contained QR encoder (byte mode, ECC M, v2/v3) --- */
        var GF_EXP = new Array(512), GF_LOG = new Array(256);
        (function () {
          var x = 1;
          for (var i = 0; i < 255; i++) { GF_EXP[i] = x; GF_LOG[x] = i; x <<= 1; if (x & 0x100) x ^= 0x11d; }
          for (var j = 255; j < 512; j++) GF_EXP[j] = GF_EXP[j - 255];
        })();
        function gmul(a, b) { return (a === 0 || b === 0) ? 0 : GF_EXP[GF_LOG[a] + GF_LOG[b]]; }
        function rsGenPoly(n) { /* highest-degree-first, monic */
          var poly = [1];
          for (var i = 0; i < n; i++) {
            var next = new Array(poly.length + 1).fill(0);
            for (var k = 0; k < poly.length; k++) { next[k] ^= poly[k]; next[k + 1] ^= gmul(poly[k], GF_EXP[i]); }
            poly = next;
          }
          return poly;
        }
        function rsEcc(data, eccLen) {
          var gen = rsGenPoly(eccLen);
          var rem = data.slice().concat(new Array(eccLen).fill(0));
          for (var i = 0; i < data.length; i++) {
            var f = rem[i];
            if (f === 0) continue;
            for (var j = 1; j < gen.length; j++) rem[i + j] ^= gmul(gen[j], f);
          }
          return rem.slice(data.length);
        }
        var VERSIONS = { 2: [44, 16, 28], 3: [70, 26, 44] };
        var ALIGN = { 2: 18, 3: 22 };
        function buildCodewords(bytes, ver) {
          var spec = VERSIONS[ver], dataCap = spec[2], bits = [];
          function push(val, len) { for (var i = len - 1; i >= 0; i--) bits.push((val >>> i) & 1); }
          push(4, 4); push(bytes.length, 8);
          for (var i = 0; i < bytes.length; i++) push(bytes[i], 8);
          push(0, Math.min(4, dataCap * 8 - bits.length));
          while (bits.length % 8 !== 0) bits.push(0);
          var data = [];
          for (var b = 0; b < bits.length; b += 8) {
            var v = 0;
            for (var k = 0; k < 8; k++) v = (v << 1) | bits[b + k];
            data.push(v);
          }
          var PAD = [0xEC, 0x11], pi = 0;
          while (data.length < dataCap) data.push(PAD[pi++ % 2]);
          return data.concat(rsEcc(data, spec[1]));
        }
        function makeMatrix(ver) {
          var size = 17 + 4 * ver, m = [];
          for (var r = 0; r < size; r++) m.push(new Array(size).fill(null));
          function finder(cy, cx) {
            for (var dy = -1; dy <= 7; dy++) for (var dx = -1; dx <= 7; dx++) {
              var y = cy + dy, x = cx + dx;
              if (y < 0 || y >= size || x < 0 || x >= size) continue;
              var inArea = (dy >= 0 && dy <= 6 && dx >= 0 && dx <= 6);
              m[y][x] = inArea ? ((dy === 0 || dy === 6 || dx === 0 || dx === 6) || (dy >= 2 && dy <= 4 && dx >= 2 && dx <= 4)) : false;
            }
          }
          finder(0, 0); finder(0, size - 7); finder(size - 7, 0);
          for (var t2 = 8; t2 < size - 8; t2++) { m[6][t2] = (t2 % 2 === 0); m[t2][6] = (t2 % 2 === 0); }
          var ac = ALIGN[ver];
          for (var dy2 = -2; dy2 <= 2; dy2++) for (var dx2 = -2; dx2 <= 2; dx2++) {
            var yy = ac + dy2, xx = ac + dx2;
            if (m[yy][xx] !== null) continue;
            m[yy][xx] = Math.max(Math.abs(dy2), Math.abs(dx2)) !== 1;
          }
          m[size - 8][8] = true; /* dark module */
          /* reserve the 30 format cells so placement never eats data bits */
          for (var f = 0; f < 8; f++) m[8][size - 1 - f] = false;
          m[8][7] = false;
          for (f = 9; f < 15; f++) m[8][15 - 1 - f] = false;
          for (f = 0; f < 6; f++) m[f][8] = false;
          m[7][8] = false; m[8][8] = false;
          for (f = 8; f < 15; f++) m[size - 15 + f][8] = false;
          return m;
        }
        function maskTest(y, x, mask) {
          switch (mask) {
            case 0: return (y + x) % 2 === 0;
            case 1: return y % 2 === 0;
            case 2: return x % 3 === 0;
            case 3: return (y + x) % 3 === 0;
            case 4: return (Math.floor(y / 2) + Math.floor(x / 3)) % 2 === 0;
            case 5: return (y * x) % 2 + (y * x) % 3 === 0;
            case 6: return ((y * x) % 2 + (y * x) % 3) % 2 === 0;
            default: return ((y + x) % 2 + (y * x) % 3) % 2 === 0;
          }
        }
        function placeData(m, cw, mask) {
          var size = m.length, bitIdx = 0, totalBits = cw.length * 8, upward = true, col = size - 1;
          while (col > 0) {
            if (col === 6) col--;
            for (var i = 0; i < size; i++) {
              var y = upward ? size - 1 - i : i;
              for (var c = 0; c < 2; c++) {
                var x = col - c;
                if (m[y][x] !== null) continue;
                var dark = false;
                if (bitIdx < totalBits) { dark = ((cw[bitIdx >> 3] >> (7 - (bitIdx & 7))) & 1) === 1; bitIdx++; }
                if (maskTest(y, x, mask)) dark = !dark;
                m[y][x] = dark;
              }
            }
            upward = !upward; col -= 2;
          }
        }
        function formatBits(mask) {
          var data = mask, fmt = data << 10, g = 0x537;
          for (var i = 14; i >= 10; i--) if ((fmt >> i) & 1) fmt ^= g << (i - 10);
          return ((data << 10) | fmt) ^ 0x5412;
        }
        function drawFormat(m, mask) {
          var size = m.length, val = formatBits(mask), i;
          for (i = 0; i < 8; i++) m[8][size - 1 - i] = ((val >> i) & 1) === 1;
          m[8][7] = ((val >> 8) & 1) === 1;
          for (i = 9; i < 15; i++) m[8][15 - 1 - i] = ((val >> i) & 1) === 1;
          for (i = 0; i < 6; i++) m[i][8] = ((val >> i) & 1) === 1;
          m[7][8] = ((val >> 6) & 1) === 1;
          m[8][8] = ((val >> 7) & 1) === 1;
          for (i = 8; i < 15; i++) m[size - 15 + i][8] = ((val >> i) & 1) === 1;
        }
        function penalty(m) {
          var size = m.length, score = 0, y, x, k;
          function lineRuns(get) {
            var run = 1;
            for (var i = 1; i < size; i++) {
              if (get(i) === get(i - 1)) { run++; if (i === size - 1 && run >= 5) score += 3 + run - 5; }
              else { if (run >= 5) score += 3 + run - 5; run = 1; }
            }
          }
          for (y = 0; y < size; y++) lineRuns(function (i) { return m[y][i]; });
          for (x = 0; x < size; x++) lineRuns(function (i) { return m[i][x]; });
          for (y = 0; y < size - 1; y++) for (x = 0; x < size - 1; x++) {
            var v = m[y][x];
            if (m[y][x + 1] === v && m[y + 1][x] === v && m[y + 1][x + 1] === v) score += 3;
          }
          var P1 = [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0], P2 = [0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1];
          function finderish(get) {
            for (var i = 0; i < size - 10; i++) {
              var ok1 = true, ok2 = true;
              for (k = 0; k < 11; k++) {
                var v2 = get(i + k);
                if (v2 !== P1[k]) ok1 = false;
                if (v2 !== P2[k]) ok2 = false;
                if (!ok1 && !ok2) break;
              }
              if (ok1 || ok2) score += 40;
            }
          }
          for (y = 0; y < size; y++) finderish(function (i) { return m[y][i]; });
          for (x = 0; x < size; x++) finderish(function (i) { return m[i][x]; });
          var dark = 0;
          for (y = 0; y < size; y++) for (x = 0; x < size; x++) if (m[y][x]) dark++;
          score += Math.floor(Math.abs(dark * 100 / (size * size) - 50) / 5) * 10;
          return score;
        }
        var bytes = [];
        for (var i3 = 0; i3 < nvQrUrl.length; i3++) {
          var c3 = nvQrUrl.charCodeAt(i3);
          if (c3 < 0x80) bytes.push(c3);
          else if (c3 < 0x800) bytes.push(0xC0 | (c3 >> 6), 0x80 | (c3 & 63));
          else bytes.push(0xE0 | (c3 >> 12), 0x80 | ((c3 >> 6) & 63), 0x80 | (c3 & 63));
        }
        var ver = bytes.length <= 28 ? 2 : (bytes.length <= 44 ? 3 : null);
        if (!ver) return null; /* never on this site; card stays absent */
        var cw = buildCodewords(bytes, ver), best = null, bestScore = Infinity;
        for (var mk = 0; mk < 8; mk++) {
          var mm = makeMatrix(ver);
          placeData(mm, cw, mk);
          drawFormat(mm, mk);
          var s = penalty(mm);
          if (s < bestScore) { bestScore = s; best = mm; }
        }
        return best;
      })();
      if (nvQr) {
        qrCard = document.createElement('div');
        qrCard.className = 'qr-card';
        var qrH = document.createElement('h2');
        qrH.className = 'qr-title';
        qrH.setAttribute('data-i18n', 'dl.qr.title');
        qrH.textContent = t('dl.qr.title', getLang());
        var qrCanvas = document.createElement('canvas');
        var CELLS = nvQr.length + 8, PX = 8; /* 4-module quiet zone x2 */
        qrCanvas.width = CELLS * PX;
        qrCanvas.height = CELLS * PX;
        qrCanvas.setAttribute('data-i18n-aria', 'dl.qr.alt');
        qrCanvas.setAttribute('aria-label', t('dl.qr.alt', getLang()));
        qrCanvas.setAttribute('role', 'img');
        var qctx = qrCanvas.getContext('2d');
        if (qctx) {
          qctx.fillStyle = '#ffffff';
          qctx.fillRect(0, 0, qrCanvas.width, qrCanvas.height);
          qctx.fillStyle = '#111111';
          for (var my = 0; my < nvQr.length; my++) {
            for (var mx = 0; mx < nvQr.length; mx++) {
              if (nvQr[my][mx]) qctx.fillRect((mx + 4) * PX, (my + 4) * PX, PX, PX);
            }
          }
          qrCard.appendChild(qrH);
          qrCard.appendChild(qrCanvas);
          var qrP = document.createElement('p');
          qrP.className = 'qr-sub';
          qrP.setAttribute('data-i18n', 'dl.qr.sub');
          qrP.textContent = t('dl.qr.sub', getLang());
          qrCard.appendChild(qrP);
          var dlContainer = document.querySelector('.dl-hero .container');
          dlContainer.appendChild(qrCard);
          qrCan = qrCanvas;
        }
      }
    }
  } catch (_) { /* QR card never breaks the download page */ }

  // 16) "Save as PDF" chip (r134) — legal trio only. The print stylesheet is
  //     verified on real paper (r133: tokens, hidden chrome, RTL runs), so a
  //     one-tap path to it is pure value; the chip sits after the .page-toc
  //     toolbar, outside the nav element (it is a page action, not a ToC
  //     link). Built at engine eval (pre-paint, zero CLS); window.print()
  //     needs no capability checks. Hidden on paper by the r134 print block.
  try {
    if (/\/(terms|privacy|refund)\.html$/.test(location.pathname) && document.querySelector('.page-toc')) {
      var pcRow = document.createElement('div');
      pcRow.className = 'print-row';
      var pcBtn = document.createElement('button');
      pcBtn.type = 'button';
      pcBtn.className = 'print-chip';
      pcBtn.setAttribute('data-i18n', 'legal.print');
      pcBtn.textContent = t('legal.print', getLang());
      pcBtn.addEventListener('click', function () { window.print(); });
      pcRow.appendChild(pcBtn);
      document.querySelector('.page-toc').insertAdjacentElement('afterend', pcRow);
    }
  } catch (_) { /* print chip never breaks a legal page */ }

  applyLang(getLang());
  // Re-apply once the DOM is fully parsed: pages load i18n.js before
  // trailing content (e.g. the pricing checkout modal), which the first
  // pass cannot see. Idempotent — re-applies the same language.
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () { applyLang(getLang()); });
  }
})();
