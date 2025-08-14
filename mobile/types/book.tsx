export type Page = {
  page_number: number;
  content: string;
  ambient?: string;
};

export type Chapter = {
  chapter_number: number;
  title?: string;
  pages: Page[];
};

export type Book = {
  id: string | number;
  title?: string;
  chapters: Chapter[];
};
