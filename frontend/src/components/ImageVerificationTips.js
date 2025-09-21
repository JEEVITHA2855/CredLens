import React from 'react';
import { Image as ImageIcon, Search } from 'lucide-react';

const ImageVerificationTips = () => (
  <div className="bg-white rounded-lg border border-purple-200 p-4 mt-4">
    <div className="flex items-center space-x-2 mb-2">
      <ImageIcon className="w-4 h-4 text-purple-700" />
      <h4 className="text-sm font-semibold text-purple-900">Image/Video Verification</h4>
    </div>
    <ul className="text-sm text-purple-800 space-y-1 list-disc list-inside">
      <li>Use reverse image search (Google Images or TinEye) to find the original context</li>
      <li>Check timestamps and locations: old media is often reused for new events</li>
      <li>Look for visual anomalies: mismatched shadows, artifacts, or watermarks</li>
      <li>Compare multiple reputable sources before sharing</li>
    </ul>
    <div className="text-xs text-purple-700 mt-2 inline-flex items-center space-x-1">
      <Search className="w-3 h-3" />
      <span>Tip: Drag-and-drop an image into images.google.com to search</span>
    </div>
  </div>
);

export default ImageVerificationTips;
