import {MappingConfig} from './types';
import {IMAGE_SOURCE_MAPPINGS} from './config';

function decodeUri(uri: string) {
  if (!uri) {
    return [uri];
  }

  const result = uri.split('://');
  const address = result[1].split('/');

  return [result[0], ...address];
}

function encodeUri(decodedUri: string[]) {
  return `${decodedUri[0]}://${decodedUri.slice(1).join('/')}`;
}

export function getImageSource(uri: string, ignorePort?: boolean, config?: MappingConfig) {
  config = config || IMAGE_SOURCE_MAPPINGS;
  const decoded = decodeUri(uri);

  if (ignorePort) {
    decoded[1] = decoded[1].split(':')[0];
  }

  if (config[decoded[1]]) {
    decoded[1] = config[decoded[1]];
  }

  return encodeUri(decoded);
}
