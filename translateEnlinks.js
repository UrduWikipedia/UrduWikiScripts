// https://ur.wikipedia.org/wiki/میڈیاویکی:Gadget-Peshkar-translateEnlinks.js

var peshkarTranslateLinks = (function() {

    // صفحہ کے سرخ انگریزی روابط اخذ کرنے کے لیے
    function getSurkhRabt() {
        return new Promise((resolve, reject) => {
            const pageName = mw.config.get('wgPageName');
            const params = {
                action: 'query',
                generator: 'links',
                titles: pageName,
                gpllimit: 'max',
                format: 'json'
            };

            const mwapi = new mw.Api();
            mwapi.get(params).done(async function(data) {
                if (data && data.query && data.query.pages) {
                    const pages = data.query.pages;
                    let missingPages = [];
                    for (const p in pages) {
                        if (pages.hasOwnProperty(p) && pages[p].hasOwnProperty('missing')) {
                            const englishRegex = /^[A-Za-z0-9\s\-_(),]*$/;
                            if (englishRegex.test(pages[p].title)) {
                                const urduTitle = await getUrduTitle(pages[p].title);
                                missingPages.push({
                                    english: pages[p].title,
                                    urdu: urduTitle
                                });
                            }
                        }
                    }
                    resolve(missingPages);
                } else {
                    resolve([]);
                }
            }).fail(function(error) {
                reject(error);
            });
        });
    }

    // مربوط اردو صفحہ اخذ کرنے کے لیے
    async function getUrduTitle(englishTitle) {
        const endpoint = 'https://en.wikipedia.org/w/api.php';
        const params = new URLSearchParams({
            action: 'query',
            titles: englishTitle,
            prop: 'langlinks',
            lllang: 'ur',
            format: 'json',
            formatversion: 2
        });

        try {
            const response = await fetch(`${endpoint}?origin=*&${params.toString()}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            const data = await response.json();
            if (data.query && data.query.pages) {
                const page = data.query.pages[0];
                if (page.langlinks && page.langlinks.length > 0) {
                    return page.langlinks[0].title;
                } else {
                    return 'No Urdu title found';
                }
            }
        } catch (error) {
            console.error('API request failed:', error);
            return 'Error fetching Urdu title';
        }
    }

    // روابط کا ترجمہ کرنے کے لیے
    async function translateEnlinks(text) {
        const missingPages = await getSurkhRabt();
        missingPages.forEach(page => {
            if (page.urdu !== 'No Urdu title found' && page.urdu !== 'Error fetching Urdu title') {
                const englishTitleRegex = new RegExp(`\\[\\[(${page.english.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&')})(\\|[^\\]]+)?\\]\\]`, 'g');
                text = text.replace(englishTitleRegex, (match, p1, p2) => {
                    let displayText = p2 ? p2.slice(1) : ''; // اصل ربط
                    let pipeText = p2 ? p2 : ''; // ربط کا عنوان
                    // کیا ربط کا عنوان اردو میں ہے
                    if (/[\u0600-\u06FF]/.test(displayText)) {
                        // اگر اردو میں ہے تو عنوان کو باقی رکھیں اور محض ربط کو اردو میں منتقل کریں
                        return `[[${page.urdu}${pipeText}]]`;
                    } else {
                        // بصورت دیگر انگریزی ربط اور انگریزی عنوان دونوں کو اردو ربط سے بدلیں
                        return `[[${page.urdu}]]`;
                    }
                });
            }
        });
        return text;
    }

    return {
        translateEnlinks: translateEnlinks
    };
}());

if (typeof window !== "undefined") {
    window.peshkarTranslateLinks = peshkarTranslateLinks;
}
