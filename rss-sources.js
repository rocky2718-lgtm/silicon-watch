// ── RSS 來源設定 ─────────────────────────────────────────────────────────────
const RSS_SOURCES = [
  {
    id: 'technews',
    name: '科技新報',
    color: '#f0c060',
    badge: 'badge-technews',
    url: 'https://technews.tw/feed/',
    categories: ['market','process','material'],
  },
  {
    id: 'digitimes',
    name: 'Digitimes',
    color: '#5dc8ff',
    badge: 'badge-digitimes',
    url: 'https://www.digitimes.com/rss/rss.asp',
    categories: ['market','equipment','packaging'],
  },
  {
    id: 'liberty',
    name: '自由時報',
    color: '#00e5aa',
    badge: 'badge-liberty',
    url: 'https://ec.ltn.com.tw/rss/business.xml',
    categories: ['market'],
  },
  {
    id: 'ctimes',
    name: '工商時報',
    color: '#c0a8ff',
    badge: 'badge-ctimes',
    url: 'https://www.ctee.com.tw/rss.xml',
    categories: ['market','process'],
  },
  {
    id: 'tsmc',
    name: '台積電',
    color: '#ff8899',
    badge: 'badge-tsmc',
    url: 'https://pr.tsmc.com/tsmcpr/rss?lang=zh',
    categories: ['tsmc','process'],
  },
  {
    id: 'anandtech',
    name: 'AnandTech',
    color: '#888',
    badge: 'badge-anand',
    url: 'https://www.anandtech.com/rss/',
    categories: ['process','equipment'],
  },
];

// ── 半導體關鍵字過濾（符合任一即收錄）──────────────────────────────────────
const KEYWORDS = [
  '半導體','晶片','晶圓','製程','封裝','台積電','tsmc','samsung','intel',
  '奈米','nm ','n2','n3','n4','n5','n7','gaafet','nsfet','finfet',
  'euv','euvl','asml','極紫外光','微影','光罩','光阻',
  'hbm','cowos','soic','chiplet','異質整合','3d ic',
  '矽','二氧化矽','氮化矽','氧化鉿','high-k','low-k','介電',
  '銅製程','鎢','釕','cobalt','ruthenium',
  'semiconductor','wafer','lithography','deposition','etching',
  'foundry','fabless','ic design','記憶體','dram','nand',
];

function containsKeyword(text) {
  const lower = (text || '').toLowerCase();
  return KEYWORDS.some(k => lower.includes(k));
}
