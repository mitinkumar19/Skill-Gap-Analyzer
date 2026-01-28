import React from 'react';
import { motion } from 'framer-motion';

export interface CategoryData {
    category: string;
    your_count: number;
    required: number;
    percentage: number;
    gap: number;
}

interface SkillCategoryBreakdownProps {
    data: CategoryData[];
}

export const SkillCategoryBreakdown: React.FC<SkillCategoryBreakdownProps> = ({ data }) => {
    return (
        <div className="space-y-8 py-4">
            {data.map((item, index) => (
                <div key={item.category} className="group flex flex-col gap-2">
                    <div className="flex justify-between items-end">
                        <div className="flex items-center gap-2">
                            <span className="font-semibold text-foreground group-hover:text-primary transition-colors text-lg">
                                {item.category}
                            </span>
                            {item.gap > 0 && (
                                <div className="relative group/dot">
                                    <div className="w-2 h-2 rounded-full bg-destructive animate-pulse" />
                                    <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 px-2 py-1 bg-card border border-border shadow-soft rounded text-[10px] opacity-0 group-hover/dot:opacity-100 transition-opacity whitespace-nowrap z-50">
                                        Gap: {item.gap} skills
                                    </div>
                                </div>
                            )}
                        </div>
                        <div className="text-sm font-medium text-muted-foreground">
                            <span className="text-primary font-bold">{item.your_count}</span>
                            <span className="mx-1">/</span>
                            <span>{item.required} ({item.percentage}%)</span>
                        </div>
                    </div>

                    <div className="relative h-4 w-full bg-muted/30 rounded-full overflow-hidden">
                        {/* Required (Background/Outline) */}
                        <div
                            className="absolute inset-0 h-full border-2 border-purple-500/30 rounded-full z-0"
                            style={{ width: '100%' }}
                        />
                        {/* Required Shadow/Hollow Bar */}
                        <div
                            className="absolute inset-0 h-full bg-purple-500/10 rounded-full z-0"
                            style={{ width: '100%' }}
                        />

                        {/* Your Skills (Foreground) */}
                        <motion.div
                            initial={{ width: 0 }}
                            animate={{ width: `${item.percentage}%` }}
                            transition={{ duration: 1, delay: index * 0.1, ease: "easeOut" }}
                            className="absolute h-full bg-blue-500 rounded-full z-10 shadow-[0_0_15px_rgba(59,130,246,0.3)]"
                        />
                    </div>

                    {/* Subtle hover details */}
                    <div className="h-0 opacity-0 group-hover:h-5 group-hover:opacity-100 transition-all text-xs text-muted-foreground flex gap-4">
                        <span className="flex items-center gap-1">
                            <div className="w-2 h-2 rounded-full bg-blue-500" /> Your Skills
                        </span>
                        <span className="flex items-center gap-1">
                            <div className="w-2 h-2 rounded-full border border-purple-500" /> Required
                        </span>
                    </div>
                </div>
            ))}
        </div>
    );
};
