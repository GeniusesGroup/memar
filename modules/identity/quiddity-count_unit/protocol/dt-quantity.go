/* For license and copyright information please see the LEGAL file in the code repository */

package qcu_p

type Field_Quantity interface {
	Quantity() Quantity
}

// Quiddity
// TODO::: decimal >> 1.5 >> 1.2 >> 10 >> 0
type Quantity int64
