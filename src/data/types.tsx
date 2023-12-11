/**
 * 排行榜上的用户信息
 */
export interface UserOnRank {
	/**
	 * 用户id
	 */
	id: number
	/**
	 * 用户名
	 */
	name: string
	/**
	 * 用户分数
	 */
	score: number
}

/**
 * 挑战信息
 */
export interface GameInfo {
	/**
	 * 项目id
	 */
	id: number
	/**
	 * 项目名称
	 */
	name: string
	/**
	 * 项目描述
	 */
	desc: string
	imgUrl: string
}

/**
 * 项目信息
 */
export interface ProjectInfo {
	/**
	 * 项目类型
	 */
	typename: string
	/**
	 * 游戏列表
	 */
	games: GameInfo[]
}

/**
 * 获取项目列表的DTO
 */
export type getProjectsDTO = {
	/**
	 * 状态码
	 */
	code: number
	/**
	 * 项目列表
	 */
	data: ProjectInfo[]
	/**
	 * 信息
	 */
	msg: string
}

/**
 * 获取排行榜的DTO
 */
export type getRankDTO = {
	/**
	 * 状态码
	 */
	code: number
	/**
	 * 项目列表
	 */
	data: UserOnRank[]
	/**
	 * 信息
	 */
	msg: string
}
