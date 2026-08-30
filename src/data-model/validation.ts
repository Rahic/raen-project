import type { Embedding, MomentCluster } from "./types.js";

export function validateEmbedding(embedding: Embedding): void {
  if (!embedding.id) throw new Error("Embedding ID is required");
  if (!embedding.model) throw new Error("Embedding model is required");
  if (embedding.dimension <= 0) throw new Error("Embedding dimension must be positive");
  if (embedding.vector.length !== embedding.dimension) {
    throw new Error(`Embedding dimension mismatch: expected ${embedding.dimension}, got ${embedding.vector.length}`);
  }
}

export function validateMomentCluster(cluster: MomentCluster): void {
  if (!cluster.id) throw new Error("Cluster ID is required");
  if (!cluster.eventPackageId) throw new Error("eventPackageId is required");
  if (cluster.confidence < 0 || cluster.confidence > 1) throw new Error("Cluster confidence must be between 0 and 1");
  if (!cluster.assetIds || cluster.assetIds.length === 0) throw new Error("Moment cluster must contain at least one asset");
}



