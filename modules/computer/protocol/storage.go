/* For license and copyright information please see the LEGAL file in the code repository */

package cp

type Node interface {
	NodeID()
	Addr() // TODO::: IP, GP
}
