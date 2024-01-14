/* For license and copyright information please see the LEGAL file in the code repository */

package ltrtp

type Type uint64

const (
	Type_Unset Type = (1 << iota)
	Type_Citation

	// TODO::: right or wrong?
	Type_Localization
)
