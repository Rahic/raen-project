export type ID = string;

export type EmbeddingType = "visual" | "text" | "multimodal";

export interface Embedding {
  id: ID;
  type: EmbeddingType;
  model: string;
  dimension: number;
  vector: number[];
  createdAt: string;
}

export interface AssetMetadata {
  filename?: string;
  mimeType?: string;
  width?: number;
  height?: number;
  durationMs?: number;
  capturedAt?: string;
  source?: string;
  tags?: string[];
  extra?: Record<string, unknown>;
}

export interface Asset {
  id: ID;
  uri: string;
  metadata: AssetMetadata;
  embeddings: Embedding[];
}

export interface EventPackage {
  id: ID;
  name?: string;
  startTime?: string;
  endTime?: string;
  assetIds: ID[];
  metadata?: Record<string, unknown>;
  createdAt: string;
}

export interface MomentCluster {
  id: ID;
  eventPackageId: ID;
  assetIds: ID[];
  centroid?: number[];
  confidence: number;
  startTime?: string;
  endTime?: string;
  metadata?: Record<string, unknown>;
}
