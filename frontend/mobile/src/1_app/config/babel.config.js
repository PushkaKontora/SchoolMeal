// eslint-disable-next-line no-undef
module.exports = function(api) {
  api.cache(true);
  return {
    presets: ['babel-preset-expo', 'module:metro-react-native-babel-preset'],
    'plugins': [
      [/*'module:react-native-dotenv', {
        'moduleName': '@env',
        'path': '.env',
        'blacklist': null,
        'whitelist': null,
        'safe': true,
        'allowUndefined': true
      },*/
        'react-native-reanimated/plugin',
        '@babel/plugin-proposal-export-namespace-from']
    ]
  };
};
