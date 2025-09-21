import React from 'react';
import { ExternalLink } from 'lucide-react';

const RESOURCES = [
  { name: 'PIB Fact Check (India)', url: 'https://factcheck.pib.gov.in/' },
  { name: 'WHO Mythbusters', url: 'https://www.who.int/emergencies/diseases/novel-coronavirus-2019/advice-for-public/myth-busters' },
  { name: 'Snopes', url: 'https://www.snopes.com/' },
  { name: 'PolitiFact', url: 'https://www.politifact.com/' },
  { name: 'Google Fact Check Explorer', url: 'https://toolbox.google.com/factcheck/explorer' },
];

const ResourceLinks = () => (
  <div className="bg-white rounded-lg border border-green-200 p-4 mt-4">
    <h4 className="text-sm font-semibold text-green-900 mb-2">Trusted Resources</h4>
    <ul className="text-sm space-y-1">
      {RESOURCES.map((r) => (
        <li key={r.url}>
          <a href={r.url} target="_blank" rel="noopener noreferrer" className="text-green-700 hover:text-green-900 inline-flex items-center space-x-1">
            <ExternalLink className="w-3 h-3" />
            <span>{r.name}</span>
          </a>
        </li>
      ))}
    </ul>
  </div>
);

export default ResourceLinks;
