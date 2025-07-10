@import Cocoa;
@import MetalKit;

@interface MTKViewDelegateImpl : NSObject<MTKViewDelegate> {
}
@end

@implementation MTKViewDelegateImpl {
}
- (void)drawInMTKView:(nonnull MTKView *)view {
    MTLClearColor clearto = {(double)rand() / RAND_MAX, (double)rand() / RAND_MAX, (double)rand() / RAND_MAX, 1.0};
    view.clearColor = clearto;
    id<MTLDevice> device = [view device];
    id<MTLCommandQueue> queue = [device newCommandQueue];
    id<MTLCommandBuffer> command = [queue commandBuffer];
    MTLRenderPassDescriptor* pass = view.currentRenderPassDescriptor;
    id<MTLRenderCommandEncoder> encoder = [command renderCommandEncoderWithDescriptor:pass];
    [encoder endEncoding];
    id <CAMetalDrawable> drawable = view.currentDrawable;
    if (drawable != nil) {
        [command presentDrawable:drawable];
    }
    [command commit];
    return;
}
- (void)mtkView:(nonnull MTKView *)view drawableSizeWillChange:(CGSize)size {
}
@end

int main(int argc, const char * argv[]) {
    @autoreleasepool {
        NSApplication* application = [NSApplication sharedApplication];
        NSRect size = {{64, 64}, {640, 480}};
        NSWindow* window = [[NSWindow alloc] initWithContentRect:size styleMask:NSWindowStyleMaskTitled backing:NSBackingStoreBuffered defer:false];
        MTKView* view = [[MTKView alloc] init];
        view.device = MTLCreateSystemDefaultDevice();
        view.preferredFramesPerSecond = 1;
        MTKViewDelegateImpl* renderer = [[MTKViewDelegateImpl alloc] init];
        view.delegate = renderer;
        [window setContentView:view];
        [window makeKeyAndOrderFront: nil];
        [application run];
    }
    return 0;
}
