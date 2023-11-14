/* For license and copyright information please see the LEGAL file in the code repository */

package chaparkhane

type security struct {
	planetBlackList  map[[2]byte]*blackList
	societyBlackList map[[6]byte]*blackList
	routerBlackList  map[[10]byte]*blackList
	userBlackList    map[[14]byte]*blackList
}

type blackList struct {
}
