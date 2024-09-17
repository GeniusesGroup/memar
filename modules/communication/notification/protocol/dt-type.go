/* For license and copyright information please see the LEGAL file in the code repository */

package np

type DeliveryType uint8

const (
	DeliveryType_Unset DeliveryType = iota

	// exactly-once message processing means that the side effects are guaranteed to be applied once.
	DeliveryType_ExactlyOnce

	// at-least-once message processing means that the side effects may be applied multiple times but they may never be skipped.
	DeliveryType_AtLeastOnce

	// At-most-once message processing means that for each message sent,
	// the side effects of its processing may either be missing or applied once.
	DeliveryType_AtMostOnce
)
