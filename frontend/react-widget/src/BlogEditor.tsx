import React from 'react';
import ReactQuill from 'react-quill';
import 'react-quill/dist/quill.snow.css';
export default function BlogEditor({ value, onChange }: { value: string, onChange: (v: string) => void}) {
  return <ReactQuill value={value} onChange={onChange} />;
}