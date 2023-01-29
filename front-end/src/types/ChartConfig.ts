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
  // url?: string;
  // description?: string;
  // xKey?: string;
  // yKey?: string;
  // zKey?: string;
  // formatTickX?: Function,
  // formatTickY?: Function,
  // includeCaption?: boolean,
  // caption?: string,
  // xTicks?: number|Array<number>|Function,
}