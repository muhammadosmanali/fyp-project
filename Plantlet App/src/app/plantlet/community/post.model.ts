

export interface Post {
    description: string;
    postImage: string;
    postDate: string;
    likes: number;
    disLikes: number;
    userId: number;
}

export class PostModel {
    constructor(
        public posts: Post[] = []
    ) {}
}
