
export class PostDetailModel {
    constructor(
        public description: string,
        public postImage: string,
        public postDate: string,
        public likes: number,
        public disLikes: number,
        public userId: number
    ) {}
}
