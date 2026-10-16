import type { QueryKey, UseMutationOptions, UseMutationResult, UseQueryOptions, UseQueryResult } from '@tanstack/react-query';
import type { BenchmarkResult, Bill, CheckDeliveryAvailabilityParams, CouponInput, DeliveryAvailability, FoodItem, HealthStatus, OrderInput } from './api.schemas';
import { customFetch } from '../custom-fetch';
import type { ErrorType, BodyType } from '../custom-fetch';
type AwaitedInput<T> = PromiseLike<T> | T;
type Awaited<O> = O extends AwaitedInput<infer T> ? T : never;
type SecondParameter<T extends (...args: never) => unknown> = Parameters<T>[1];
export declare const getHealthCheckUrl: () => string;
/**
 * Returns server health status
 * @summary Health check
 */
export declare const healthCheck: (options?: Parameters<typeof customFetch>[1]) => Promise<HealthStatus>;
export declare const getHealthCheckQueryKey: () => readonly ["/api/healthz"];
export declare const getHealthCheckQueryOptions: <TData = Awaited<ReturnType<typeof healthCheck>>, TError = ErrorType<unknown>>(options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof healthCheck>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}) => UseQueryOptions<Awaited<ReturnType<typeof healthCheck>>, TError, TData> & {
    queryKey: QueryKey;
};
export type HealthCheckQueryResult = NonNullable<Awaited<ReturnType<typeof healthCheck>>>;
export type HealthCheckQueryError = ErrorType<unknown>;
/**
 * @summary Health check
 */
export declare function useHealthCheck<TData = Awaited<ReturnType<typeof healthCheck>>, TError = ErrorType<unknown>>(options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof healthCheck>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}): UseQueryResult<TData, TError> & {
    queryKey: QueryKey;
};
export declare const getGetApiHealthUrl: () => string;
/**
 * @summary API health
 */
export declare const getApiHealth: (options?: Parameters<typeof customFetch>[1]) => Promise<HealthStatus>;
export declare const getGetApiHealthQueryKey: () => readonly ["/api/health"];
export declare const getGetApiHealthQueryOptions: <TData = Awaited<ReturnType<typeof getApiHealth>>, TError = ErrorType<unknown>>(options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof getApiHealth>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}) => UseQueryOptions<Awaited<ReturnType<typeof getApiHealth>>, TError, TData> & {
    queryKey: QueryKey;
};
export type GetApiHealthQueryResult = NonNullable<Awaited<ReturnType<typeof getApiHealth>>>;
export type GetApiHealthQueryError = ErrorType<unknown>;
/**
 * @summary API health
 */
export declare function useGetApiHealth<TData = Awaited<ReturnType<typeof getApiHealth>>, TError = ErrorType<unknown>>(options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof getApiHealth>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}): UseQueryResult<TData, TError> & {
    queryKey: QueryKey;
};
export declare const getGetMenuUrl: () => string;
/**
 * @summary Get the current menu
 */
export declare const getMenu: (options?: Parameters<typeof customFetch>[1]) => Promise<FoodItem[]>;
export declare const getGetMenuQueryKey: () => readonly ["/api/menu"];
export declare const getGetMenuQueryOptions: <TData = Awaited<ReturnType<typeof getMenu>>, TError = ErrorType<unknown>>(options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof getMenu>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}) => UseQueryOptions<Awaited<ReturnType<typeof getMenu>>, TError, TData> & {
    queryKey: QueryKey;
};
export type GetMenuQueryResult = NonNullable<Awaited<ReturnType<typeof getMenu>>>;
export type GetMenuQueryError = ErrorType<unknown>;
/**
 * @summary Get the current menu
 */
export declare function useGetMenu<TData = Awaited<ReturnType<typeof getMenu>>, TError = ErrorType<unknown>>(options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof getMenu>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}): UseQueryResult<TData, TError> & {
    queryKey: QueryKey;
};
export declare const getCalculateOrderUrl: () => string;
/**
 * @summary Calculate an order without saving it
 */
export declare const calculateOrder: (orderInput: OrderInput, options?: Parameters<typeof customFetch>[1]) => Promise<Bill>;
export declare const getCalculateOrderMutationKey: () => readonly ["calculateOrder"];
export declare const getCalculateOrderMutationOptions: <TError = ErrorType<void>, TContext = unknown>(options?: {
    mutation?: UseMutationOptions<Awaited<ReturnType<typeof calculateOrder>>, TError, CalculateOrderMutationVariables, TContext>;
    request?: SecondParameter<typeof customFetch>;
}) => UseMutationOptions<Awaited<ReturnType<typeof calculateOrder>>, TError, CalculateOrderMutationVariables, TContext>;
export type CalculateOrderMutationResult = NonNullable<Awaited<ReturnType<typeof calculateOrder>>>;
export type CalculateOrderMutationBody = BodyType<OrderInput>;
export type CalculateOrderMutationError = ErrorType<void>;
export type CalculateOrderMutationVariables = {
    data: BodyType<OrderInput>;
};
/**
* @summary Calculate an order without saving it
*/
export declare const useCalculateOrder: <TError = ErrorType<void>, TContext = unknown>(options?: {
    mutation?: UseMutationOptions<Awaited<ReturnType<typeof calculateOrder>>, TError, CalculateOrderMutationVariables, TContext>;
    request?: SecondParameter<typeof customFetch>;
}) => UseMutationResult<Awaited<ReturnType<typeof calculateOrder>>, TError, CalculateOrderMutationVariables, TContext>;
export declare const getCreateOrderUrl: () => string;
/**
 * @summary Save an order and calculate its bill
 */
export declare const createOrder: (orderInput: OrderInput, options?: Parameters<typeof customFetch>[1]) => Promise<Bill>;
export declare const getCreateOrderMutationKey: () => readonly ["createOrder"];
export declare const getCreateOrderMutationOptions: <TError = ErrorType<void>, TContext = unknown>(options?: {
    mutation?: UseMutationOptions<Awaited<ReturnType<typeof createOrder>>, TError, CreateOrderMutationVariables, TContext>;
    request?: SecondParameter<typeof customFetch>;
}) => UseMutationOptions<Awaited<ReturnType<typeof createOrder>>, TError, CreateOrderMutationVariables, TContext>;
export type CreateOrderMutationResult = NonNullable<Awaited<ReturnType<typeof createOrder>>>;
export type CreateOrderMutationBody = BodyType<OrderInput>;
export type CreateOrderMutationError = ErrorType<void>;
export type CreateOrderMutationVariables = {
    data: BodyType<OrderInput>;
};
/**
* @summary Save an order and calculate its bill
*/
export declare const useCreateOrder: <TError = ErrorType<void>, TContext = unknown>(options?: {
    mutation?: UseMutationOptions<Awaited<ReturnType<typeof createOrder>>, TError, CreateOrderMutationVariables, TContext>;
    request?: SecondParameter<typeof customFetch>;
}) => UseMutationResult<Awaited<ReturnType<typeof createOrder>>, TError, CreateOrderMutationVariables, TContext>;
export declare const getGetOrderBillUrl: (orderId: string) => string;
/**
 * @summary Recalculate a saved order's bill
 */
export declare const getOrderBill: (orderId: string, options?: Parameters<typeof customFetch>[1]) => Promise<Bill>;
export declare const getGetOrderBillMutationKey: () => readonly ["getOrderBill"];
export declare const getGetOrderBillMutationOptions: <TError = ErrorType<void>, TContext = unknown>(options?: {
    mutation?: UseMutationOptions<Awaited<ReturnType<typeof getOrderBill>>, TError, GetOrderBillMutationVariables, TContext>;
    request?: SecondParameter<typeof customFetch>;
}) => UseMutationOptions<Awaited<ReturnType<typeof getOrderBill>>, TError, GetOrderBillMutationVariables, TContext>;
export type GetOrderBillMutationResult = NonNullable<Awaited<ReturnType<typeof getOrderBill>>>;
export type GetOrderBillMutationError = ErrorType<void>;
export type GetOrderBillMutationVariables = {
    orderId: string;
};
/**
* @summary Recalculate a saved order's bill
*/
export declare const useGetOrderBill: <TError = ErrorType<void>, TContext = unknown>(options?: {
    mutation?: UseMutationOptions<Awaited<ReturnType<typeof getOrderBill>>, TError, GetOrderBillMutationVariables, TContext>;
    request?: SecondParameter<typeof customFetch>;
}) => UseMutationResult<Awaited<ReturnType<typeof getOrderBill>>, TError, GetOrderBillMutationVariables, TContext>;
export declare const getApplyOrderCouponUrl: (orderId: string) => string;
/**
 * @summary Apply a coupon to a saved order
 */
export declare const applyOrderCoupon: (orderId: string, couponInput: CouponInput, options?: Parameters<typeof customFetch>[1]) => Promise<Bill>;
export declare const getApplyOrderCouponMutationKey: () => readonly ["applyOrderCoupon"];
export declare const getApplyOrderCouponMutationOptions: <TError = ErrorType<void>, TContext = unknown>(options?: {
    mutation?: UseMutationOptions<Awaited<ReturnType<typeof applyOrderCoupon>>, TError, ApplyOrderCouponMutationVariables, TContext>;
    request?: SecondParameter<typeof customFetch>;
}) => UseMutationOptions<Awaited<ReturnType<typeof applyOrderCoupon>>, TError, ApplyOrderCouponMutationVariables, TContext>;
export type ApplyOrderCouponMutationResult = NonNullable<Awaited<ReturnType<typeof applyOrderCoupon>>>;
export type ApplyOrderCouponMutationBody = BodyType<CouponInput>;
export type ApplyOrderCouponMutationError = ErrorType<void>;
export type ApplyOrderCouponMutationVariables = {
    orderId: string;
    data: BodyType<CouponInput>;
};
/**
* @summary Apply a coupon to a saved order
*/
export declare const useApplyOrderCoupon: <TError = ErrorType<void>, TContext = unknown>(options?: {
    mutation?: UseMutationOptions<Awaited<ReturnType<typeof applyOrderCoupon>>, TError, ApplyOrderCouponMutationVariables, TContext>;
    request?: SecondParameter<typeof customFetch>;
}) => UseMutationResult<Awaited<ReturnType<typeof applyOrderCoupon>>, TError, ApplyOrderCouponMutationVariables, TContext>;
export declare const getCheckDeliveryAvailabilityUrl: (params: CheckDeliveryAvailabilityParams) => string;
/**
 * @summary Demonstrate concurrent delivery availability checks
 */
export declare const checkDeliveryAvailability: (params: CheckDeliveryAvailabilityParams, options?: Parameters<typeof customFetch>[1]) => Promise<DeliveryAvailability>;
export declare const getCheckDeliveryAvailabilityQueryKey: (params?: CheckDeliveryAvailabilityParams) => readonly ["/api/delivery/availability", ...CheckDeliveryAvailabilityParams[]];
export declare const getCheckDeliveryAvailabilityQueryOptions: <TData = Awaited<ReturnType<typeof checkDeliveryAvailability>>, TError = ErrorType<unknown>>(params: CheckDeliveryAvailabilityParams, options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof checkDeliveryAvailability>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}) => UseQueryOptions<Awaited<ReturnType<typeof checkDeliveryAvailability>>, TError, TData> & {
    queryKey: QueryKey;
};
export type CheckDeliveryAvailabilityQueryResult = NonNullable<Awaited<ReturnType<typeof checkDeliveryAvailability>>>;
export type CheckDeliveryAvailabilityQueryError = ErrorType<unknown>;
/**
 * @summary Demonstrate concurrent delivery availability checks
 */
export declare function useCheckDeliveryAvailability<TData = Awaited<ReturnType<typeof checkDeliveryAvailability>>, TError = ErrorType<unknown>>(params: CheckDeliveryAvailabilityParams, options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof checkDeliveryAvailability>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}): UseQueryResult<TData, TError> & {
    queryKey: QueryKey;
};
export declare const getRunBillingBenchmarkUrl: () => string;
/**
 * @summary Measure billing computation at increasing order sizes
 */
export declare const runBillingBenchmark: (options?: Parameters<typeof customFetch>[1]) => Promise<BenchmarkResult>;
export declare const getRunBillingBenchmarkQueryKey: () => readonly ["/api/performance/benchmark"];
export declare const getRunBillingBenchmarkQueryOptions: <TData = Awaited<ReturnType<typeof runBillingBenchmark>>, TError = ErrorType<unknown>>(options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof runBillingBenchmark>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}) => UseQueryOptions<Awaited<ReturnType<typeof runBillingBenchmark>>, TError, TData> & {
    queryKey: QueryKey;
};
export type RunBillingBenchmarkQueryResult = NonNullable<Awaited<ReturnType<typeof runBillingBenchmark>>>;
export type RunBillingBenchmarkQueryError = ErrorType<unknown>;
/**
 * @summary Measure billing computation at increasing order sizes
 */
export declare function useRunBillingBenchmark<TData = Awaited<ReturnType<typeof runBillingBenchmark>>, TError = ErrorType<unknown>>(options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof runBillingBenchmark>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}): UseQueryResult<TData, TError> & {
    queryKey: QueryKey;
};
export {};
//# sourceMappingURL=api.d.ts.map