import { describe, it, expect } from 'vitest';
import fs from 'fs';

describe('assets folder', () => {
  it('contains at least one file', () => {
    const files = fs.readdirSync('data/originals');
    expect(files.length).toBeGreaterThan(0);
  });
});
