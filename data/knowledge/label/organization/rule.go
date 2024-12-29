/* For license and copyright information please see the LEGAL file in the code repository */

package label

// logic-type:::
/*
	It means rule will execute only by call related service.
	e.g. apply a voucher on an invoice just by enter voucher code by user in related input element.
	Manual

	Time information indicate in calendar domain
	Repeatable

	Trigger when desire `Event` dispatched
	EventBase

	It will part of process and can change the flow of the desire service (process)
	e.g. by return an error.
	((Synchronous == false) == ASynchronous) It will call beside or after process and can't change the flow of the services.
	Synchronous

	It means rule not valid after a certain of times.
	TimeLimit
*/

// Discount or product-auction, sales, ...
// to reduce invoices price automatically by some rules
// Discount

// Voucher or gift voucher is a bond of the redeemable transaction type which is worth a certain monetary value and
// which may be spent only for specific reasons or on specific products
// Voucher

// GiftProduct
// UserClubCoin
// Refund

// Government cash or gift product to poor people
// Subsidy
