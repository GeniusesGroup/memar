/* For license and copyright information please see the LEGAL file in the code repository */

package anp

type Node interface {
	NodeID()
	Addr() // TODO::: IP, GP
}

// protocol.EventTarget
