import { Route, type RouteObject } from "react-router-dom";

import { ROUTES } from "../shared/constants";

import React from "react";

import { lazy } from "react";
const Params = lazy(() => import('../features/Tabs/Params'));
const Basic = lazy(() => import('../features/Tabs/Basic'));
const Payments = lazy(() => import("../features/Tabs/Payments"));
const Results = lazy(() => import("../features/Tabs/Results"));

export const routes: RouteObject[] = [
    {
        path: ROUTES.params,
        element: React.createElement(Params)
    },

    {
        path: ROUTES.basic,
        element: React.createElement(Basic),
    },

    {
        path: ROUTES.payments,
        element: React.createElement(Payments),
    },

    {
        path: ROUTES.results,
        element: React.createElement(Results),
    }
]
