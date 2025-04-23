/* For license and copyright information please see the LEGAL file in the code repository */

package all_or_none

// [transaction, `all_or_none`, ----] >>

// Policy (rule):::
// Whole order must be filled for matching deal or order must cancelled on timeout
// If this flag absent, allow matching engine to deal part of order.
// https://en.wikipedia.org/wiki/All_or_none
// an order that must be executed in its entirety, or not executed at all
//
// https://en.wikipedia.org/wiki/Fill_or_kill
// an order that must be executed immediately"—a few seconds, customarily—in its entirety;
// otherwise, the entire order is cancelled; no partial fulfillments are allowed.
// Type_FillOrKill = Type_AllOrNone & Type_Duration
// Fill-or-Kill Budget (FOK-B)
