// src/utils/constants.js

export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const CATEGORIES = [
'Food','Transport','Entertainment','Shopping','Utilities','Healthcare','Education','Personal','Others'
];

export const CATEGORY_COLORS = {
  Food: '#FF6B6B',
  Transport: '#4ECDC4',
  Entertainment: '#FFE66D',
  Shopping: '#95E1D3',
  Utilities: '#FF8B94',
  Healthcare: '#C7CEEA',
  Education: '#FFDAC1',
  Personal: '#865432ff',
  Others: '#B4B4B4'
};

export const CATEGORY_EMOJI = {
  Food: '🍔',
  Transport: '🚗',
  Entertainment: '🎬',
  Shopping: '🛍️',
  Utilities: '🔨' ,
  Healthcare: '🏥',
  Education: '📚',
  Personal: '😇',
  Others: '📦'
};