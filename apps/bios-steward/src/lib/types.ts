export interface EvidenceFixture {
  id: string;
  domain: string;
  title: string;
  status: "draft_synthetic";
  purpose: string;
  blockedActions: string[];
}
