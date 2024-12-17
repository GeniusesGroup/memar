/* For license and copyright information please see the LEGAL file in the code repository */

package is_p

import (
	qsp "org/modules/identity/quiddity-status/protocol"
)

type Field_Status interface {
	InvoiceStatus() Status
}

type Status qsp.Quiddity_Status

const (
	// cancelled : Indicates that you have cancelled the invoice. Though you can view the cancelled invoice,
	// the customer cannot view the invoice or make payments against the invoice.
	// You can only cancel an unpaid issued invoice.
	// invoice is no longer valid, and not payable by client or refund
	Status_Voided = Status(qsp.Quiddity_Status_FreeFlag << iota)

	// expired : Indicates that an invoice has expired. Once expired,
	// the customer cannot make any payments against the invoice,
	// and you cannot cancel or delete the invoice. You can view an expired invoice.
	// Status_Expired

	// partially paid : Indicates that the customer has made a partial payment against an invoice.
	// After a payment has been made, you can neither delete nor cancel the invoice.
	// You can only view the invoice and add internal notes to it.
	Status_PartiallyPaid

	// paid : Indicates that the customer has fully paid the invoice amount.
	// Paid is the final state of an invoice. A paid invoice can only be viewed.
	// You can neither delete nor cancel it.
	Status_Paid

	Status_UserCheckout
	Status_PendingReview
	Status_Confirmed // Approved
	Status_Packaging
	Status_Shipping
	Status_Done // delivered or served
)

// 0//created 1//ManagerApprove 2//WarehouseApprove 3//ActiveWithApprove 4//ActiveWithoutApprove
// 5//ActiveWithOrderer 6//Inactive 7//Normal 8//Reject 9//Void
