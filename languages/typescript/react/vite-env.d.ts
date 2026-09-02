/// <reference types="vite/client" />

// Typed Vite env: only VITE_* variables are exposed to the client.
interface ImportMetaEnv {
  readonly VITE_APP_NAME: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
