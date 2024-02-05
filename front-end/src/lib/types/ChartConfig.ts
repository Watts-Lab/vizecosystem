export default interface ChartConfig {
  type: string;
  rScale: Function;
  rDomain: number[];
  rRange: number[];
  zScale: Function;
  zDomain: number[];
  colorInterpolator: Function;
  colorInterpolatorDomain: number[];
  colorInterpolatorScheme: string[]|string;
  colorPaletteAnchors: number[];
}
