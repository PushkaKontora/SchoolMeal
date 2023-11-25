import {ParamListBase, RouteProp} from '@react-navigation/native';

export type PropsWithNavigation = {
    navigation: any,
    route?: any
};

export type PropsWithNavigationTyped<Params extends ParamListBase> = {
    navigation: any,
    route: RouteProp<{params: Params}>
}
