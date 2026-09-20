/* For license and copyright information please see the LEGAL file in the code repository */

package planet_p

// TODO::: PlanetID not work?? we need it just in GP protocol and
// that protocol MUST implement it with a distributed algorithm.

// PlanetID indicate planet ID with some useful methods
type PlanetID uint16

const (
	Planet_UnSet PlanetID = iota
	Planet_Earth
	Planet_Mars
)
